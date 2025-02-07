from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Pattern, PatternHooksNeedle, Favourite, DIFFICULTY_LEVEL, CRAFT, WEIGHT, SIZE, CATEGORY, HOOK_SIZE, NEEDLE_SIZE, HOOK_NEEDLE_TYPE

class PatternHooksNeedleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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

    # def test_pattern_hooks_needles_str(self):
    #     hook = PatternHooksNeedle.objects.create(
    #         pattern=self.pattern,
    #         type=HOOK_NEEDLE_TYPE[0][0],  # Hook
    #         hook_size=HOOK_SIZE[0][0]  # 2.0 mm
    #     )
    #     needle = PatternHooksNeedle.objects.create(
    #         pattern=self.pattern,
    #         type=HOOK_NEEDLE_TYPE[1][0],  # Needle
    #         needle_size=NEEDLE_SIZE[0][0]  # 2.0 mm / US 0
    #     )

    #     self.assertEqual(str(hook), f"Hook for {self.pattern.title} by {self.pattern.author.username}")
    #     self.assertEqual(str(needle), f"Needle for {self.pattern.title} by {self.pattern.author.username}")

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
        self.user = User.objects.create_user(username='testuser', password='12345')
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

    # def test_pattern_str(self):
    #     self.assertEqual(str(self.pattern), f"{self.pattern.title} made by {self.pattern.author.username}")

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
            description='This is a test pattern with an invalid difficulty level.',
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
        self.user = User.objects.create_user(username='testuser', password='12345')
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
        self.favourite = Favourite.objects.create(
            user=self.user,
            pattern=self.pattern
        )

    def test_favourite_creation(self):
        self.assertEqual(self.favourite.user, self.user)
        self.assertEqual(self.favourite.pattern, self.pattern)

    # def test_favourite_str(self):
    #     self.assertEqual(str(self.favourite), f"{self.user.username} favourite")

    def test_create_favourite_without_user(self):
        with self.assertRaises(IntegrityError):
            Favourite.objects.create(
                pattern=self.pattern
            )

    def test_create_favourite_without_pattern(self):
        favourite = Favourite(
            user=self.user
        )
        favourite.full_clean()  # This should not raise any errors
        favourite.save()
        self.assertEqual(favourite.user, self.user)
        self.assertIsNone(favourite.pattern)

    # def test_create_favourite_with_nonexistent_user(self):
    #     with self.assertRaises(IntegrityError):
    #             Favourite.objects.create(
    #                 user_id=9999,  # Nonexistent user ID
    #                 pattern=self.pattern
    #             )

    # def test_create_favourite_with_nonexistent_pattern(self):
    #     with transaction.atomic():
    #         with self.assertRaises(IntegrityError):
    #             Favourite.objects.create(
    #                 user=self.user,
    #                 pattern_id=9999  # Nonexistent pattern ID
    #             )

    # def test_create_duplicate_favourite(self):
    #     with self.assertRaises(IntegrityError):
    #         Favourite.objects.create(
    #             user=self.user,
    #             pattern=self.pattern
            # )

    # def test_update_favourite_user(self):
    #     new_user = User.objects.create_user(username='newuser', password='12345')
    #     self.favourite.user = new_user
    #     self.favourite.save()
    #     self.assertEqual(self.favourite.user, new_user)

    # def test_update_favourite_pattern(self):
    #     new_pattern = Pattern.objects.create(
    #         author=self.user,
    #         title='New Test Pattern',
    #         description='This is a new test pattern.',
    #         difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
    #         craft=CRAFT[0][0],  # Crochet
    #         yarn_weight=WEIGHT[0][0],  # Lace/2 ply
    #         size=SIZE[0][0],  # One Size
    #         category=CATEGORY[0][0],  # Clothing
    #     )
    #     self.favourite.pattern = new_pattern
    #     self.favourite.save()
    #     self.assertEqual(self.favourite.pattern, new_pattern)