from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Pattern, Favourite, Comment, DIFFICULTY_LEVEL, CRAFT,
    WEIGHT, SIZE, CATEGORY, HOOK_SIZE, HOOK_NEEDLE_TYPE
)
from .forms import PatternForm, PatternHooksNeedleFormSet


class PatternListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern1 = Pattern.objects.create(
            author=self.user,
            title='Test Pattern 1',
            slug='test-pattern-1',
            description='This is test pattern 1.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        self.pattern2 = Pattern.objects.create(
            author=self.user,
            title='Test Pattern 2',
            slug='test-pattern-2',
            description='This is test pattern 2.',
            difficulty_level=DIFFICULTY_LEVEL[1][0],  # Medium
            craft=CRAFT[1][0],  # Knitting
            yarn_weight=WEIGHT[1][0],  # Light Fingering/3 ply
            size=SIZE[1][0],  # XS
            category=CATEGORY[1][0],  # Accessories
        )

    def test_pattern_list_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_pattern_list_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'patterns/index.html')

    def test_pattern_list_view_context(self):
        response = self.client.get(reverse('home'))
        self.assertIn('object_list', response.context)
        self.assertEqual(len(response.context['object_list']), 2)

    def test_pattern_list_view_pagination(self):
        for i in range(10):
            Pattern.objects.create(
                author=self.user,
                title=f'Test Pattern {i+3}',
                slug=f'test-pattern-{i+3}',
                description=f'This is test pattern {i+3}.',
                difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
                craft=CRAFT[0][0],  # Crochet
                yarn_weight=WEIGHT[0][0],  # Lace/2 ply
                size=SIZE[0][0],  # One Size
                category=CATEGORY[0][0],  # Clothing
            )
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['is_paginated'])
        # paginate_by is set to 8
        self.assertEqual(len(response.context['object_list']), 8)

    def test_pattern_list_view_favourite_patterns(self):
        self.client.login(username='testuser', password='12345')
        favourite, created = Favourite.objects.get_or_create(user=self.user)
        favourite.pattern.set([self.pattern1])
        response = self.client.get(reverse('home'))
        self.assertIn('favourite_patterns', response.context)
        self.assertEqual(len(response.context['favourite_patterns']), 1)
        self.assertIn(self.pattern1, response.context['favourite_patterns'])


class PatternDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            slug='test-pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )

    def test_pattern_detail_view_status_code(self):
        response = self.client.get(
            reverse('pattern_detail', args=[self.pattern.slug]))
        self.assertEqual(response.status_code, 200)

    def test_pattern_detail_view_template(self):
        response = self.client.get(
            reverse('pattern_detail', args=[self.pattern.slug]))
        self.assertTemplateUsed(response, 'patterns/pattern_detail.html')

    def test_pattern_detail_view_context(self):
        response = self.client.get(
            reverse('pattern_detail', args=[self.pattern.slug]))
        self.assertIn('pattern', response.context)
        self.assertEqual(response.context['pattern'], self.pattern)

    def test_pattern_detail_view_comments(self):
        comment = Comment.objects.create(
            author=self.user,
            pattern=self.pattern,
            content='This is a test comment.'
        )
        response = self.client.get(
            reverse('pattern_detail', args=[self.pattern.slug]))
        self.assertIn('comments', response.context)
        self.assertEqual(len(response.context['comments']), 1)
        self.assertIn(comment, response.context['comments'])

    def test_pattern_detail_view_favourite_patterns(self):
        self.client.login(username='testuser', password='12345')
        favourite, created = Favourite.objects.get_or_create(user=self.user)
        favourite.pattern.set([self.pattern])
        response = self.client.get(
            reverse('pattern_detail', args=[self.pattern.slug]))
        self.assertIn('favourite_patterns', response.context)
        self.assertEqual(len(response.context['favourite_patterns']), 1)
        self.assertIn(self.pattern, response.context['favourite_patterns'])

    def test_pattern_detail_view_post_comment(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('pattern_detail', args=[self.pattern.slug]),
            {'content': 'This is a test comment.'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content,
                         'This is a test comment.')


class ToggleFavouriteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            slug='test-pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )

    def test_toggle_favourite_add(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('toggle_favourite', args=[self.pattern.slug]))
        self.assertRedirects(response, reverse(
            'pattern_detail', args=[self.pattern.slug]))
        favourite = Favourite.objects.get(user=self.user)
        self.assertIn(self.pattern, favourite.pattern.all())

    def test_toggle_favourite_remove(self):
        self.client.login(username='testuser', password='12345')
        favourite, created = Favourite.objects.get_or_create(user=self.user)
        favourite.pattern.set([self.pattern])
        response = self.client.post(
            reverse('toggle_favourite', args=[self.pattern.slug]))
        self.assertRedirects(response, reverse(
            'pattern_detail', args=[self.pattern.slug]))
        favourite.refresh_from_db()
        self.assertNotIn(self.pattern, favourite.pattern.all())

    def test_toggle_favourite_redirect(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('toggle_favourite', args=[self.pattern.slug]),
            HTTP_REFERER=reverse('home')
        )
        self.assertRedirects(response, reverse('home'))


class EditCommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            slug='test-pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        self.comment = Comment.objects.create(
            author=self.user,
            pattern=self.pattern,
            content='This is a test comment.'
        )

    def test_edit_comment_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('edit_comment', args=[self.pattern.slug, self.comment.id]),
            {'content': 'This is an updated test comment.'}
        )
        # Redirects after successful edit
        self.assertEqual(response.status_code, 302)

    def test_edit_comment_view_content_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('edit_comment', args=[self.pattern.slug, self.comment.id]),
            {'content': 'This is an updated test comment.'}
        )
        # Redirects after successful edit
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content,
                         'This is an updated test comment.')

    def test_edit_comment_view_invalid_user(self):
        User.objects.create_user(
            username='otheruser', password='12345')
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(
            reverse('edit_comment', args=[self.pattern.slug, self.comment.id]),
            {'content': 'This is an updated test comment.'}
        )
        # Redirects after failed edit
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content,
                            'This is an updated test comment.')

    def test_edit_comment_view_no_login(self):
        response = self.client.post(
            reverse('edit_comment', args=[self.pattern.slug, self.comment.id]),
            {'content': 'This is an updated test comment.'}
        )
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content,
                            'This is an updated test comment.')


class DeleteCommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            slug='test-pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        self.comment = Comment.objects.create(
            author=self.user,
            pattern=self.pattern,
            content='This is a test comment.'
        )

    def test_delete_comment_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('delete_comment',
                    args=[self.pattern.slug, self.comment.id]))
        # Redirects after successful delete
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_view_comment_deleted(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('delete_comment',
                    args=[self.pattern.slug, self.comment.id]))
        # Redirects after successful delete
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)

    def test_delete_comment_view_invalid_user(self):
        User.objects.create_user(
            username='otheruser', password='12345')
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(
            reverse('delete_comment',
                    args=[self.pattern.slug, self.comment.id]))
        # Redirects after failed delete
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_view_no_login(self):
        response = self.client.post(
            reverse('delete_comment',
                    args=[self.pattern.slug, self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())


class PostPatternViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_post_pattern_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_pattern'))
        self.assertEqual(response.status_code, 200)

    def test_post_pattern_view_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_pattern'))
        self.assertTemplateUsed(response, 'patterns/post_pattern.html')

    def test_post_pattern_view_form(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_pattern'))
        self.assertIsInstance(response.context['form'], PatternForm)
        self.assertIsInstance(
            response.context['formset'], PatternHooksNeedleFormSet)

    def test_post_pattern_view_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_pattern'), {
            'title': 'New Test Pattern',
            'description': 'This is a new test pattern.',
            'difficulty_level': DIFFICULTY_LEVEL[0][0],  # Easy
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'pattern_hooks_needles-0-hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'pattern_hooks_needles-0-needle_size': '',
        })
        # Redirects after successful post
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pattern.objects.count(), 1)
        self.assertEqual(Pattern.objects.first().title, 'New Test Pattern')

    def test_post_pattern_view_invalid_form(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_pattern'), {
            'title': '',
            'description': 'This is a new test pattern.',
            'difficulty_level': DIFFICULTY_LEVEL[0][0],  # Easy
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'pattern_hooks_needles-0-hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'pattern_hooks_needles-0-needle_size': '',
        })
        # Renders the form again with errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Pattern.objects.count(), 0)
        form = response.context['form']
        self.assertFormError(form, 'title', 'This field is required.')


class FavouriteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern1 = Pattern.objects.create(
            author=self.user,
            title='Test Pattern 1',
            slug='test-pattern-1',
            description='This is test pattern 1.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        self.pattern2 = Pattern.objects.create(
            author=self.user,
            title='Test Pattern 2',
            slug='test-pattern-2',
            description='This is test pattern 2.',
            difficulty_level=DIFFICULTY_LEVEL[1][0],  # Medium
            craft=CRAFT[1][0],  # Knitting
            yarn_weight=WEIGHT[1][0],  # Light Fingering/3 ply
            size=SIZE[1][0],  # XS
            category=CATEGORY[1][0],  # Accessories
        )
        self.favourite, created = Favourite.objects.get_or_create(
            user=self.user)
        self.favourite.pattern.set([self.pattern1, self.pattern2])

    def test_favourite_view_status_code(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('favourite'))
        self.assertEqual(response.status_code, 200)

    def test_favourite_view_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('favourite'))
        self.assertTemplateUsed(response, 'favourite/favourite.html')

    def test_favourite_view_context(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('favourite'))
        self.assertIn('patterns', response.context)
        self.assertEqual(len(response.context['patterns']), 2)
        self.assertIn(self.pattern1, response.context['patterns'])
        self.assertIn(self.pattern2, response.context['patterns'])

    def test_favourite_view_no_login(self):
        response = self.client.get(reverse('favourite'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(
            response,
            f"{reverse('account_login')}?next={reverse('favourite')}")
