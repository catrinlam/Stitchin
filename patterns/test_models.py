from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import (
    Pattern, PatternHooksNeedle, Favourite, Comment, DIFFICULTY_LEVEL, CRAFT,
    WEIGHT, SIZE, CATEGORY, HOOK_SIZE, NEEDLE_SIZE, HOOK_NEEDLE_TYPE
)


class PatternHooksNeedleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )

    def test_pattern_hooks_needles_creation(self):
        hook = PatternHooksNeedle.objects.create(
            pattern=self.pattern,
            type=HOOK_NEEDLE_TYPE[0][0],  # Hook
            hook_size=HOOK_SIZE[0][0]  # 2.0 mm
        )
        needle = PatternHooksNeedle.objects.create(
            pattern=self.pattern,
            type=HOOK_NEEDLE_TYPE[1][0],  # Needle
            needle_size=NEEDLE_SIZE[0][0]  # 2.0 mm / US 0
        )

        self.assertEqual(hook.pattern, self.pattern)
        self.assertEqual(hook.type, HOOK_NEEDLE_TYPE[0][0])
        self.assertEqual(hook.hook_size, HOOK_SIZE[0][0])
        self.assertIsNone(hook.needle_size)

        self.assertEqual(needle.pattern, self.pattern)
        self.assertEqual(needle.type, HOOK_NEEDLE_TYPE[1][0])
        self.assertEqual(needle.needle_size, NEEDLE_SIZE[0][0])
        self.assertIsNone(needle.hook_size)

    def test_pattern_hooks_needles_str(self):
        hook = PatternHooksNeedle.objects.create(
            pattern=self.pattern,
            type=HOOK_NEEDLE_TYPE[0][0],  # Hook
            hook_size=HOOK_SIZE[0][0]  # 2.0 mm
        )
        needle = PatternHooksNeedle.objects.create(
            pattern=self.pattern,
            type=HOOK_NEEDLE_TYPE[1][0],  # Needle
            needle_size=NEEDLE_SIZE[0][0]  # 2.0 mm / US 0
        )

        self.assertEqual(
                str(hook),
                f"Hook for {self.pattern.title} by "
                f"{self.pattern.author.username}"
            )
        self.assertEqual(
                str(needle),
                f"Needle for {self.pattern.title} by "
                f"{self.pattern.author.username}"
            )

    def test_create_pattern_hooks_needles_without_type(self):
        with self.assertRaises(ValidationError):
            hook = PatternHooksNeedle(
                pattern=self.pattern,
                hook_size=HOOK_SIZE[0][0]  # 2.0 mm
            )
            hook.full_clean()

    def test_create_pattern_hooks_needles_without_pattern(self):
        with self.assertRaises(IntegrityError):
            PatternHooksNeedle.objects.create(
                type=HOOK_NEEDLE_TYPE[0][0],  # Hook
                hook_size=HOOK_SIZE[0][0]  # 2.0 mm
            )

    def test_create_pattern_hooks_needles_with_invalid_type(self):
        with self.assertRaises(ValidationError):
            hook = PatternHooksNeedle(
                pattern=self.pattern,
                type=99,  # Invalid type
                hook_size=HOOK_SIZE[0][0]  # 2.0 mm
            )
            hook.full_clean()

    def test_create_pattern_hooks_needles_with_invalid_hook_size(self):
        with self.assertRaises(ValidationError):
            hook = PatternHooksNeedle(
                pattern=self.pattern,
                type=HOOK_NEEDLE_TYPE[0][0],  # Hook
                hook_size=99  # Invalid hook size
            )
            hook.full_clean()

    def test_create_pattern_hooks_needles_with_invalid_needle_size(self):
        with self.assertRaises(ValidationError):
            needle = PatternHooksNeedle(
                pattern=self.pattern,
                type=HOOK_NEEDLE_TYPE[1][0],  # Needle
                needle_size=99  # Invalid needle size
            )
            needle.full_clean()


class PatternModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )

    def test_pattern_creation(self):
        self.assertEqual(self.pattern.author, self.user)
        self.assertEqual(self.pattern.title, 'Test Pattern')
        self.assertEqual(self.pattern.description, 'This is a test pattern.')
        self.assertEqual(self.pattern.difficulty_level, DIFFICULTY_LEVEL[0][0])
        self.assertEqual(self.pattern.craft, CRAFT[0][0])
        self.assertEqual(self.pattern.yarn_weight, WEIGHT[0][0])
        self.assertEqual(self.pattern.size, SIZE[0][0])
        self.assertEqual(self.pattern.category, CATEGORY[0][0])

    def test_create_pattern_without_title(self):
        pattern = Pattern(
            author=self.user,
            description='This is a test pattern without a title.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        with self.assertRaises(ValidationError):
            pattern.full_clean()

    def test_create_pattern_without_author(self):
        with self.assertRaises(IntegrityError):
            Pattern.objects.create(
                title='Test Pattern without Author',
                description='This is a test pattern without an author.',
                difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
                craft=CRAFT[0][0],  # Crochet
                yarn_weight=WEIGHT[0][0],  # Lace/2 ply
                size=SIZE[0][0],  # One Size
                category=CATEGORY[0][0],  # Clothing
            )

    def test_create_pattern_with_invalid_difficulty_level(self):
        pattern = Pattern(
            author=self.user,
            title='Test Pattern with Invalid Difficulty Level',
            description=(
                'This is a test pattern with an invalid difficulty level.'
            ),
            difficulty_level=99,  # Invalid difficulty level
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        with self.assertRaises(ValidationError):
            pattern.full_clean()


class FavouriteModelTest(TestCase):
    def setUp(self):
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
        self.favourite, created = Favourite.objects.get_or_create(
            user=self.user)
        self.favourite.pattern.set([self.pattern])

    def test_favourite_creation(self):
        self.assertEqual(self.favourite.user, self.user)
        self.assertEqual(self.favourite.pattern.first(), self.pattern)

    def test_create_favourite_without_user(self):
        with self.assertRaises(ValidationError):
            favourite = Favourite()
            favourite.full_clean()

    def test_create_favourite_without_pattern(self):
        self.user2 = User.objects.create_user(
            username='testuser2', password='12345')
        favourite, created = Favourite.objects.get_or_create(user=self.user2)
        favourite.full_clean()  # This should not raise any errors
        favourite.save()
        self.assertEqual(favourite.user, self.user2)
        self.assertEqual(favourite.pattern.count(), 0)

    def test_create_duplicate_favourite(self):
        with self.assertRaises(IntegrityError):
            favourite = Favourite.objects.create(
                user=self.user,
            )
            favourite.pattern.set([self.pattern])

    def test_update_favourite_pattern(self):
        new_pattern = Pattern.objects.create(
            author=self.user,
            title='Another Test Pattern',
            slug='another-test-pattern',
            description='This is another test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        self.favourite.pattern.set([new_pattern])
        self.favourite.save()
        self.assertEqual(self.favourite.pattern.first(), new_pattern)

    def test_delete_user_deletes_favourite(self):
        user_id = self.user.id
        self.user.delete()
        self.assertEqual(Favourite.objects.count(), 0)
        with self.assertRaises(Favourite.DoesNotExist):
            Favourite.objects.get(user_id=user_id)


class CommentModelTest(TestCase):
    def setUp(self):
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

    def test_comment_creation(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.pattern, self.pattern)
        self.assertEqual(self.comment.content, 'This is a test comment.')

    def test_create_comment_without_author(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                pattern=self.pattern,
                content='This is a test comment without an author.'
            )

    def test_create_comment_without_pattern(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                author=self.user,
                content='This is a test comment without a pattern.'
            )

    def test_create_comment_without_content(self):
        with self.assertRaises(ValidationError):
            comment = Comment(
                author=self.user,
                pattern=self.pattern,
                content=''  # Empty content
            )
            comment.full_clean()

    def test_update_comment_content(self):
        self.comment.content = 'This is an updated test comment.'
        self.comment.save()
        self.assertEqual(
            self.comment.content, 'This is an updated test comment.'
        )

    def test_delete_comment(self):
        comment_id = self.comment.id
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)
