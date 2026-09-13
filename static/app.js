/**
 * TechBlog Full-Stack Blog Platform Client Script
 * Handles REST API interactions, authentication state, post feed with images,
 * interactive likes, share action, search filtering, and reader modal.
 */

const TOKEN_KEY = 'techblog_token';
let currentUser = null;
let currentActivePost = null;
let activeCategory = 'all';
let searchDebounceTimer = null;
const likedPostsSet = new Set(JSON.parse(localStorage.getItem('techblog_liked_posts') || '[]'));

// =========================================================================
// Centralized API Request Helper
// =========================================================================
async function fetchApi(endpoint, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(endpoint, {
      ...options,
      headers
    });
    const data = await response.json();
    return { status: response.status, ok: response.ok, data };
  } catch (error) {
    console.error('API Error:', error);
    return { status: 500, ok: false, data: { error: 'Network or server error occurred.' } };
  }
}

// =========================================================================
// Authentication & User State
// =========================================================================
async function fetchCurrentUser() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) {
    currentUser = null;
    return null;
  }

  const res = await fetchApi('/api/auth/me');
  if (res.ok && res.data.success) {
    currentUser = res.data.user;
    return currentUser;
  } else {
    localStorage.removeItem(TOKEN_KEY);
    currentUser = null;
    return null;
  }
}

function updateNavbar() {
  const navActions = document.getElementById('nav-actions');
  if (!navActions) return;

  if (currentUser) {
    const initial = currentUser.username.charAt(0).toUpperCase();
    navActions.innerHTML = `
      <a href="/create-post" class="btn btn-primary btn-sm">+ Write Post</a>
      <a href="/profile" class="user-badge" title="View Profile">
        <span class="user-avatar-mini">${initial}</span>
        <span>${escapeHtml(currentUser.username)}</span>
      </a>
      <button onclick="handleLogout()" class="btn btn-secondary btn-sm" title="Log out">Log Out</button>
    `;
  } else {
    navActions.innerHTML = `
      <a href="/auth" class="btn btn-secondary btn-sm">Sign In</a>
      <a href="/auth?tab=register" class="btn btn-primary btn-sm">Register</a>
    `;
  }
}

async function handleLogout() {
  await fetchApi('/api/auth/logout', { method: 'POST' });
  localStorage.removeItem(TOKEN_KEY);
  currentUser = null;
  showToast('You have been logged out.', 'success');
  updateNavbar();
  if (window.location.pathname.includes('/create-post') || window.location.pathname.includes('/profile')) {
    window.location.href = '/';
  } else {
    loadPosts();
  }
}

// =========================================================================
// Blog Feed & Search Logic (index.html)
// =========================================================================
async function loadPosts(searchQuery = '', category = activeCategory) {
  const grid = document.getElementById('posts-grid');
  const countEl = document.getElementById('feed-count');
  const emptyState = document.getElementById('empty-state');
  if (!grid) return;

  grid.innerHTML = `
    <div class="post-card-skeleton"></div>
    <div class="post-card-skeleton"></div>
    <div class="post-card-skeleton"></div>
  `;
  emptyState.style.display = 'none';

  let url = '/api/posts?';
  const params = [];
  if (searchQuery.trim()) {
    params.push(`q=${encodeURIComponent(searchQuery.trim())}`);
  }
  if (category && category.toLowerCase() !== 'all') {
    params.push(`category=${encodeURIComponent(category)}`);
  }
  url += params.join('&');

  const res = await fetchApi(url);

  if (res.ok && res.data.posts) {
    const posts = res.data.posts;
    countEl.innerText = `${posts.length} ${posts.length === 1 ? 'article' : 'articles'}`;

    if (posts.length === 0) {
      grid.innerHTML = '';
      emptyState.style.display = 'block';
      return;
    }

    grid.innerHTML = posts.map(post => {
      const readTime = Math.max(1, Math.ceil((post.content || '').split(/\s+/).length / 180));
      const postImage = post.image_url || getCategoryFallbackBanner(post.category);
      const isLiked = likedPostsSet.has(post.id);

      return `
        <article class="post-card" onclick="openPostModal(${post.id})">
          <div class="post-card-thumb-wrapper">
            <img src="${escapeHtml(postImage)}" alt="${escapeHtml(post.title)}" class="post-card-thumb" loading="lazy" />
            <span class="post-reading-time">${readTime} min read</span>
          </div>
          <div class="card-top-meta">
            <span class="card-category">${escapeHtml(post.category)}</span>
            <span class="card-date">${formatDate(post.created_at)}</span>
          </div>
          <h3 class="card-title">${escapeHtml(post.title)}</h3>
          <p class="card-excerpt">${escapeHtml(post.content)}</p>
          <div class="card-footer">
            <div class="card-author">
              <span class="user-avatar-mini" style="width:24px; height:24px; font-size:0.75rem;">${post.author_name.charAt(0).toUpperCase()}</span>
              <span>${escapeHtml(post.author_name)}</span>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
              <span class="card-comments-count" title="Likes">
                ${isLiked ? '❤️' : '🤍'} <span id="card-likes-${post.id}">${post.likes || 0}</span>
              </span>
              <span class="card-comments-count" title="Comments">
                💬 <span>${post.comment_count}</span>
              </span>
            </div>
          </div>
        </article>
      `;
    }).join('');
  } else {
    grid.innerHTML = `<p class="error-msg">Failed to load articles. Please check server connection.</p>`;
  }
}

function getCategoryFallbackBanner(category) {
  const cat = (category || '').toLowerCase();
  if (cat.includes('software')) return '/assets/software-banner.svg';
  if (cat.includes('hardware') || cat.includes('iot')) return '/assets/hardware-iot-banner.svg';
  if (cat.includes('intern')) return '/assets/internship-banner.svg';
  if (cat.includes('job')) return '/assets/jobs-banner.svg';
  return '/assets/general-banner.svg';
}

function resetFilters() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) searchInput.value = '';
  const clearBtn = document.getElementById('clear-search');
  if (clearBtn) clearBtn.style.display = 'none';

  activeCategory = 'all';
  document.querySelectorAll('.cat-pill').forEach(pill => {
    pill.classList.toggle('active', pill.dataset.category === 'all');
  });

  loadPosts('', 'all');
}

function initSearchListeners() {
  const searchInput = document.getElementById('search-input');
  const clearBtn = document.getElementById('clear-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const val = e.target.value;
    clearBtn.style.display = val ? 'block' : 'none';

    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => {
      loadPosts(val, activeCategory);
    }, 300);
  });

  clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearBtn.style.display = 'none';
    loadPosts('', activeCategory);
  });
}

function initCategoryListeners() {
  const pills = document.querySelectorAll('.cat-pill');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeCategory = pill.dataset.category;
      const searchVal = document.getElementById('search-input')?.value || '';
      loadPosts(searchVal, activeCategory);
    });
  });
}

// =========================================================================
// Post Reader Modal & Commenting Logic
// =========================================================================
async function openPostModal(postId) {
  const modal = document.getElementById('post-modal');
  const articleContainer = document.getElementById('modal-article');
  const commentsList = document.getElementById('comments-list');
  const commentForm = document.getElementById('comment-form');
  const commentLoginPrompt = document.getElementById('comment-login-prompt');
  const heroWrapper = document.getElementById('modal-hero-wrapper');
  const heroImg = document.getElementById('modal-hero-img');
  const likeBtn = document.getElementById('modal-like-btn');
  const likesCount = document.getElementById('modal-likes-count');
  const heartIcon = document.getElementById('modal-heart-icon');

  if (!modal) return;

  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  articleContainer.innerHTML = '<p class="loading-text">Loading full article...</p>';
  commentsList.innerHTML = '';

  if (currentUser) {
    commentForm.style.display = 'block';
    commentLoginPrompt.style.display = 'none';
  } else {
    commentForm.style.display = 'none';
    commentLoginPrompt.style.display = 'block';
  }

  const res = await fetchApi(`/api/posts/${postId}`);
  if (res.ok && res.data.post) {
    currentActivePost = res.data.post;
    const post = currentActivePost;

    // Display Hero Image
    const coverUrl = post.image_url || getCategoryFallbackBanner(post.category);
    heroImg.src = coverUrl;
    heroWrapper.style.display = 'block';

    // Update Likes State
    likesCount.innerText = post.likes || 0;
    const isLiked = likedPostsSet.has(post.id);
    if (isLiked) {
      likeBtn.classList.add('liked');
      heartIcon.innerText = '❤️';
    } else {
      likeBtn.classList.remove('liked');
      heartIcon.innerText = '🤍';
    }

    const readTime = Math.max(1, Math.ceil((post.content || '').split(/\s+/).length / 180));

    articleContainer.innerHTML = `
      <header class="article-header">
        <span class="article-category">${escapeHtml(post.category)}</span>
        <h1 class="article-title">${escapeHtml(post.title)}</h1>
        <div class="article-meta">
          <span>By <strong>${escapeHtml(post.author_name)}</strong></span>
          <span>•</span>
          <span>${formatDate(post.created_at)}</span>
          <span>•</span>
          <span>⏱️ ${readTime} min read</span>
        </div>
      </header>
      <div class="article-body">${escapeHtml(post.content)}</div>
    `;

    renderComments(post.comments || []);
  } else {
    articleContainer.innerHTML = `<p class="error-msg">Error loading post details.</p>`;
  }
}

// Interactive Like Handler
async function handleLikeCurrentPost() {
  if (!currentActivePost) return;
  const postId = currentActivePost.id;
  const likeBtn = document.getElementById('modal-like-btn');
  const likesCount = document.getElementById('modal-likes-count');
  const heartIcon = document.getElementById('modal-heart-icon');

  const res = await fetchApi(`/api/posts/${postId}/like`, { method: 'POST' });
  if (res.ok && res.data.success) {
    likedPostsSet.add(postId);
    localStorage.setItem('techblog_liked_posts', JSON.stringify([...likedPostsSet]));

    currentActivePost.likes = res.data.likes;
    likesCount.innerText = res.data.likes;
    likeBtn.classList.add('liked');
    heartIcon.innerText = '❤️';

    // Update card likes count in the feed background
    const cardLikesSpan = document.getElementById(`card-likes-${postId}`);
    if (cardLikesSpan) cardLikesSpan.innerText = res.data.likes;

    showToast('Post liked! ❤️', 'success');
  }
}

// Interactive Share Handler
function handleShareCurrentPost() {
  if (!currentActivePost) return;
  const url = `${window.location.origin}/?post=${currentActivePost.id}`;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url).then(() => {
      showToast('Article link copied to clipboard! 🔗', 'success');
    }).catch(() => {
      prompt('Copy this link:', url);
    });
  } else {
    prompt('Copy this link:', url);
  }
}

function renderComments(comments) {
  const commentsList = document.getElementById('comments-list');
  const commentsCount = document.getElementById('modal-comments-count');
  commentsCount.innerText = comments.length;

  if (comments.length === 0) {
    commentsList.innerHTML = `<p style="color:var(--text-dim); font-size:0.9rem; font-style:italic;">No comments yet. Be the first to share your thoughts!</p>`;
    return;
  }

  commentsList.innerHTML = comments.map(c => `
    <div class="comment-item">
      <div class="comment-header">
        <span class="comment-author-name">${escapeHtml(c.author_name)}</span>
        <span class="comment-date">${formatDate(c.created_at)}</span>
      </div>
      <div class="comment-body">${escapeHtml(c.content)}</div>
    </div>
  `).join('');
}

function closePostModal() {
  const modal = document.getElementById('post-modal');
  if (!modal) return;
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  currentActivePost = null;
}

function initModalListeners() {
  const modal = document.getElementById('post-modal');
  const closeBtn = document.getElementById('modal-close');
  const commentForm = document.getElementById('comment-form');

  if (closeBtn) closeBtn.addEventListener('click', closePostModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closePostModal();
    });
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal?.classList.contains('open')) {
      closePostModal();
    }
  });

  if (commentForm) {
    commentForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!currentActivePost || !currentUser) return;

      const textarea = document.getElementById('comment-text');
      const content = textarea.value.trim();
      if (!content) return;

      const res = await fetchApi(`/api/posts/${currentActivePost.id}/comments`, {
        method: 'POST',
        body: JSON.stringify({ content })
      });

      if (res.ok && res.data.comment) {
        textarea.value = '';
        showToast('Comment published!', 'success');
        const updatedPostRes = await fetchApi(`/api/posts/${currentActivePost.id}`);
        if (updatedPostRes.ok) {
          renderComments(updatedPostRes.data.post.comments || []);
        }
        loadPosts();
      } else {
        showToast(res.data.error || 'Failed to post comment.', 'error');
      }
    });
  }
}

// =========================================================================
// Authentication Page Handlers (auth.html)
// =========================================================================
async function handleLoginSubmit(event) {
  event.preventDefault();
  const alertBox = document.getElementById('auth-alert');
  const btn = document.getElementById('login-submit-btn');
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  alertBox.style.display = 'none';
  btn.disabled = true;
  btn.innerText = 'Signing In...';

  const res = await fetchApi('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  });

  btn.disabled = false;
  btn.innerText = 'Sign In';

  if (res.ok && res.data.user) {
    localStorage.setItem(TOKEN_KEY, res.data.user.token);
    currentUser = res.data.user;
    window.location.href = '/';
  } else {
    alertBox.style.display = 'block';
    alertBox.innerText = res.data.error || 'Invalid credentials. Please try again.';
  }
}

async function handleRegisterSubmit(event) {
  event.preventDefault();
  const alertBox = document.getElementById('auth-alert');
  const btn = document.getElementById('reg-submit-btn');
  const username = document.getElementById('reg-username').value;
  const email = document.getElementById('reg-email').value;
  const password = document.getElementById('reg-password').value;
  const bio = document.getElementById('reg-bio').value;

  alertBox.style.display = 'none';
  btn.disabled = true;
  btn.innerText = 'Creating Account...';

  const res = await fetchApi('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password, bio })
  });

  btn.disabled = false;
  btn.innerText = 'Create Account';

  if (res.ok && res.data.user) {
    localStorage.setItem(TOKEN_KEY, res.data.user.token);
    currentUser = res.data.user;
    window.location.href = '/';
  } else {
    alertBox.style.display = 'block';
    alertBox.innerText = res.data.error || 'Registration failed.';
  }
}

// =========================================================================
// Post Creation Handler (create-post.html)
// =========================================================================
async function handleCreatePostSubmit(event) {
  event.preventDefault();
  const title = document.getElementById('post-title').value;
  const category = document.getElementById('post-category').value;
  const content = document.getElementById('post-content').value;
  const image_url = document.getElementById('post-image')?.value || '';
  const alertBox = document.getElementById('editor-alert');
  const publishBtn = document.getElementById('publish-btn');

  alertBox.style.display = 'none';
  publishBtn.disabled = true;
  publishBtn.innerHTML = '<span>Publishing...</span>';

  const res = await fetchApi('/api/posts', {
    method: 'POST',
    body: JSON.stringify({ title, category, content, image_url })
  });

  publishBtn.disabled = false;
  publishBtn.innerHTML = `<span>Publish Article</span>`;

  if (res.ok && res.data.post) {
    showToast('Article published with cover image!', 'success');
    setTimeout(() => {
      window.location.href = '/';
    }, 800);
  } else {
    alertBox.className = 'alert-box auth-alert';
    alertBox.style.display = 'block';
    alertBox.innerText = res.data.error || 'Failed to publish post.';
  }
}

// =========================================================================
// Profile Page Handler (profile.html)
// =========================================================================
async function loadUserProfilePage() {
  const user = await fetchCurrentUser();
  if (!user) {
    window.location.href = '/auth';
    return;
  }

  const res = await fetchApi(`/api/users/${user.id}/profile`);
  if (!res.ok) {
    showToast('Error loading profile', 'error');
    return;
  }

  const profile = res.data.profile;
  document.getElementById('profile-avatar').innerText = profile.username.charAt(0).toUpperCase();
  document.getElementById('profile-username').innerText = profile.username;
  document.getElementById('profile-email').innerText = profile.email;
  document.getElementById('profile-bio').innerText = profile.bio || 'No bio provided yet.';
  document.getElementById('profile-posts-stat').innerText = `📚 ${profile.total_posts} ${profile.total_posts === 1 ? 'Article' : 'Articles'}`;
  document.getElementById('profile-joined-stat').innerText = `🗓️ Member since ${formatDate(profile.created_at)}`;

  const postsList = document.getElementById('user-posts-list');
  if (profile.posts.length === 0) {
    postsList.innerHTML = `<p style="color:var(--text-dim); padding: 20px 0;">You haven't published any articles yet.</p>`;
    return;
  }

  postsList.innerHTML = profile.posts.map(p => `
    <div class="user-post-item" id="post-row-${p.id}">
      <div style="display:flex; align-items:center; gap:16px;">
        <img src="${p.image_url || getCategoryFallbackBanner(p.category)}" style="width:64px; height:48px; border-radius:6px; object-fit:cover;" alt="Thumbnail" />
        <div>
          <h4 class="user-post-title">${escapeHtml(p.title)}</h4>
          <span class="card-category" style="margin-top:6px; display:inline-block;">${escapeHtml(p.category)}</span>
          <span style="font-size:0.8rem; color:var(--text-dim); margin-left:8px;">${formatDate(p.created_at)} • ❤️ ${p.likes || 0} • 💬 ${p.comment_count}</span>
        </div>
      </div>
      <div class="user-post-actions">
        <button class="btn btn-danger btn-sm" onclick="handleDeletePost(${p.id})">Delete</button>
      </div>
    </div>
  `).join('');
}

async function handleDeletePost(postId) {
  if (!confirm('Are you sure you want to delete this article? This action cannot be undone.')) {
    return;
  }

  const res = await fetchApi(`/api/posts/${postId}`, { method: 'DELETE' });
  if (res.ok) {
    showToast('Article deleted.', 'success');
    const row = document.getElementById(`post-row-${postId}`);
    if (row) row.remove();
  } else {
    showToast(res.data.error || 'Failed to delete article.', 'error');
  }
}

// =========================================================================
// Utilities (Dates, Toast, Escaping)
// =========================================================================
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}

function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.className = `toast ${type}`;
  toast.innerText = message;
  toast.style.display = 'block';

  setTimeout(() => {
    toast.style.display = 'none';
  }, 4000);
}

// =========================================================================
// App Initialization
// =========================================================================
window.addEventListener('DOMContentLoaded', async () => {
  await fetchCurrentUser();
  updateNavbar();

  if (document.getElementById('posts-grid')) {
    initSearchListeners();
    initCategoryListeners();
    initModalListeners();
    loadPosts();

    // Check if URL has ?post=<id>
    const params = new URLSearchParams(window.location.search);
    const directPostId = params.get('post');
    if (directPostId && !isNaN(directPostId)) {
      openPostModal(parseInt(directPostId));
    }
  }
});
