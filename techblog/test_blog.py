import unittest
import os

# Test in an isolated database file
os.environ["BLOG_DB_FILE"] = "test_blog.db"
import database

class BlogLogicUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists("test_blog.db"):
            os.remove("test_blog.db")
        database.init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_blog.db"):
            os.remove("test_blog.db")

    def test_01_user_registration(self):
        user, err = database.register_user(
            username="sabir_tester",
            email="tester@example.com",
            password="strongpassword123",
            bio="Test engineer bio"
        )
        self.assertIsNone(err)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "sabir_tester")
        self.assertIn("token", user)
        self.__class__.test_user = user

    def test_02_duplicate_user_rejection(self):
        user, err = database.register_user(
            username="sabir_tester",
            email="tester2@example.com",
            password="anotherpassword"
        )
        self.assertIsNone(user)
        self.assertIn("already registered", err)

    def test_03_login_validation(self):
        user, err = database.login_user("sabir_tester", "strongpassword123")
        self.assertIsNone(err)
        self.assertIsNotNone(user)

        user_bad, err_bad = database.login_user("sabir_tester", "wrongpassword")
        self.assertIsNone(user_bad)
        self.assertIn("Invalid", err_bad)

    def test_04_session_token_retrieval(self):
        token = self.__class__.test_user["token"]
        user = database.get_user_by_token(token)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "sabir_tester")

    def test_05_create_and_fetch_post_with_image(self):
        user = self.__class__.test_user
        post, err = database.create_post(
            author_id=user["id"],
            title="Optimizing ESP32 Sensor Hubs",
            content="Understanding hardware peripherals and lightweight MQTT telemetry enables scalable IoT deployments.",
            category="Hardware & IoT",
            image_url="/assets/hardware-iot-banner.svg"
        )
        self.assertIsNone(err)
        self.assertIsNotNone(post)
        self.assertEqual(post["title"], "Optimizing ESP32 Sensor Hubs")
        self.assertEqual(post["category"], "Hardware & IoT")
        self.assertEqual(post["image_url"], "/assets/hardware-iot-banner.svg")
        self.assertEqual(post["likes"], 0)
        self.__class__.created_post = post

    def test_06_like_post(self):
        post_id = self.__class__.created_post["id"]
        new_likes = database.like_post(post_id)
        self.assertEqual(new_likes, 1)

        post = database.get_post_by_id(post_id)
        self.assertEqual(post["likes"], 1)

    def test_07_search_and_merged_category(self):
        # Search by keyword
        posts = database.get_posts(search_query="Sensor")
        self.assertGreaterEqual(len(posts), 1)

        # Search by merged category "Hardware & IoT"
        hw_posts = database.get_posts(category="Hardware & IoT")
        self.assertGreaterEqual(len(hw_posts), 1)
        self.assertTrue(any("ESP32" in p["title"] for p in hw_posts))

    def test_08_commenting_system(self):
        user = self.__class__.test_user
        post_id = self.__class__.created_post["id"]

        comment, err = database.create_comment(
            post_id=post_id,
            author_id=user["id"],
            content="Super helpful post for IoT engineering students!"
        )
        self.assertIsNone(err)
        self.assertIsNotNone(comment)
        self.assertEqual(comment["content"], "Super helpful post for IoT engineering students!")

        post = database.get_post_by_id(post_id)
        self.assertGreaterEqual(len(post["comments"]), 1)

    def test_09_user_profile(self):
        user = self.__class__.test_user
        profile = database.get_user_profile(user["id"])
        self.assertIsNotNone(profile)
        self.assertEqual(profile["username"], "sabir_tester")
        self.assertGreaterEqual(profile["total_posts"], 1)

    def test_10_post_deletion_permission(self):
        user = self.__class__.test_user
        post_id = self.__class__.created_post["id"]

        success, err = database.delete_post(post_id, user_id=9999)
        self.assertFalse(success)
        self.assertIn("permission", err)

        success, err = database.delete_post(post_id, user_id=user["id"])
        self.assertTrue(success)
        self.assertIsNone(err)

        post = database.get_post_by_id(post_id)
        self.assertIsNone(post)

if __name__ == "__main__":
    unittest.main()
