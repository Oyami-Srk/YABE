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
        db.session.commit()
        self.assertEqual(p3.tags.count(), 2)
        self.assertEqual(p1.comments.count(), 0)
        c1 = Comment()
        c2 = Comment()
        c3 = Comment()
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()
        p1.add_comment(c1).add_comment(c2)
        self.assertFalse(p1.has_comment(c3))
        self.assertTrue(p1.has_comment(c1))
        self.assertEqual(p1.comments.count(), 2)
        p1.remove_comment(c3)
        p1.remove_comment(c2)
        self.assertEqual(p1.comments.count(), 1)
        self.assertEqual(c1.post_id, p1.id)
        ct = Category(title='Category 1')
        pg = Page(title='Page 1')
        db.session.add(pg)
        db.session.add(ct)
        db.session.commit()
        pg.add_post(p1)
        p1.category_id = ct.id
        pg.add_post(p1)
        db.session.commit()
        self.assertEqual(p1.pages.first(), pg)
        self.assertEqual(p1.category_id, ct.id)


if __name__ == '__main__':
    unittest.main(verbosity=2)
