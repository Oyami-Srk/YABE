import unittest
from yabe import yabe, db
from yabe.models import Post, Category, Comment, Page, Tag


class ModelCase(unittest.TestCase):
    def setUp(self):
        yabe.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post(self):
        p1 = Post(title='Test Post 1')
        p2 = Post(title='Test Post 2')
        p3 = Post(title='Test Post 3')
        t1 = Tag(content='Test Tag 1')
        t2 = Tag(content='Test Tag 2')
        t3 = Tag(content='Test Tag 3')
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        self.assertEqual(p1.tags.all(), [])
        self.assertEqual(t1.posts.all(), [])
        p1.add_tag(t1)
        p1.add_tag(t2)
        p2.add_tag(t3)
        p3.add_tag(t1)
        p3.add_tag(t2)
        p3.add_tag(t3)
        db.session.commit()
        self.assertEqual(t2.posts.count(), 2)
        self.assertEqual(p3.tags.count(), 3)
        self.assertEqual(p2.tags.first().content, 'Test Tag 3')
        self.assertTrue(p1.has_tag(t1))
        p3.remove_tag(t2)
        self.assertEqual(p3.tags.count(), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
