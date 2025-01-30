from django.test import TestCase
from django.contrib.auth.models import User
from .models import Pattern, PatternHooksNeedles, DIFFICULTY_LEVEL, CRAFT, WEIGHT, SIZE, CATEGORY, HOOK_SIZE, NEEDLE_SIZE, HOOK_NEEDLE_TYPE

class PatternHooksNeedlesModelTest(TestCase):
    def setUp(self):
        self.hook = PatternHooksNeedles.objects.create(
            type=HOOK_NEEDLE_TYPE[0][0],  # Hook
            hook_size=HOOK_SIZE[0][0]  # 2.0 mm
        )
        self.needle = PatternHooksNeedles.objects.create(
            type=HOOK_NEEDLE_TYPE[1][0],  # Needle
            needle_size=NEEDLE_SIZE[0][0]  # 2.0 mm / US 0
        )

    def test_pattern_hooks_needles_creation(self):
        self.assertEqual(self.hook.type, HOOK_NEEDLE_TYPE[0][0])
        self.assertEqual(self.hook.hook_size, HOOK_SIZE[0][0])
        self.assertIsNone(self.hook.needle_size)

        self.assertEqual(self.needle.type, HOOK_NEEDLE_TYPE[1][0])
        self.assertEqual(self.needle.needle_size, NEEDLE_SIZE[0][0])
        self.assertIsNone(self.needle.hook_size)

class PatternModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.hook = PatternHooksNeedles.objects.create(
            type=HOOK_NEEDLE_TYPE[0][0],  # Hook
            hook_size=HOOK_SIZE[0][0]  # 2.0 mm
        )
        self.pattern = Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            hook=self.hook,
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
        self.assertEqual(self.pattern.hook, self.hook)
        self.assertEqual(self.pattern.size, SIZE[0][0])
        self.assertEqual(self.pattern.category, CATEGORY[0][0])