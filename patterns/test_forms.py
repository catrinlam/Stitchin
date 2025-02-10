from django.test import TestCase
from django.contrib.auth.models import User
from .forms import (
    PatternForm, PatternHooksNeedleForm, PatternHooksNeedleFormSet, CommentForm
)
from .models import (
    Pattern, PatternHooksNeedle, DIFFICULTY_LEVEL, CRAFT, WEIGHT, SIZE,
    CATEGORY, HOOK_SIZE, HOOK_NEEDLE_TYPE
)


class PatternFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_pattern_form_valid_data(self):
        form = PatternForm(data={
            'title': 'Test Pattern',
            'description': 'This is a test pattern.',
            'difficulty_level': DIFFICULTY_LEVEL[0][0],  # Easy
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
        })
        self.assertTrue(form.is_valid())
        pattern = form.save(commit=False)
        pattern.author = self.user
        pattern.save()
        self.assertEqual(pattern.title, 'Test Pattern')
        self.assertEqual(pattern.description, 'This is a test pattern.')
        self.assertEqual(pattern.difficulty_level, DIFFICULTY_LEVEL[0][0])
        self.assertEqual(pattern.craft, CRAFT[0][0])
        self.assertEqual(pattern.yarn_weight, WEIGHT[0][0])
        self.assertEqual(pattern.size, SIZE[0][0])
        self.assertEqual(pattern.category, CATEGORY[0][0])

    def test_pattern_form_missing_title(self):
        form = PatternForm(data={
            'description': 'This is a test pattern without a title.',
            'difficulty_level': DIFFICULTY_LEVEL[0][0],  # Easy
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_pattern_form_duplicate_title(self):
        Pattern.objects.create(
            author=self.user,
            title='Test Pattern',
            description='This is a test pattern.',
            difficulty_level=DIFFICULTY_LEVEL[0][0],  # Easy
            craft=CRAFT[0][0],  # Crochet
            yarn_weight=WEIGHT[0][0],  # Lace/2 ply
            size=SIZE[0][0],  # One Size
            category=CATEGORY[0][0],  # Clothing
        )
        form = PatternForm(data={
            'title': 'Test Pattern',
            'description': 'This is a duplicate test pattern.',
            'difficulty_level': DIFFICULTY_LEVEL[0][0],  # Easy
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(
            form.errors['title'],
            [
                'A pattern with this title already exists. '
                'Please choose a different title.'
            ]
        )

    def test_pattern_form_invalid_difficulty_level(self):
        form = PatternForm(data={
            'title': 'Test Pattern with Invalid Difficulty Level',
            'description': (
                'This is a test pattern with an invalid difficulty level.'
            ),
            'difficulty_level': 99,  # Invalid difficulty level
            'craft': CRAFT[0][0],  # Crochet
            'yarn_weight': WEIGHT[0][0],  # Lace/2 ply
            'size': SIZE[0][0],  # One Size
            'category': CATEGORY[0][0],  # Clothing
        })
        self.assertFalse(form.is_valid())
        self.assertIn('difficulty_level', form.errors)
        self.assertEqual(form.errors['difficulty_level'], [
                         'Select a valid choice. 99 is not one of the '
                         'available choices.'
                         ])


class PatternHooksNeedleFormTest(TestCase):
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

    def test_pattern_hooks_needle_form_valid_data(self):
        form = PatternHooksNeedleForm(data={
            'type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'needle_size': ''
        })
        self.assertTrue(form.is_valid())
        hook = form.save(commit=False)
        hook.pattern = self.pattern
        hook.save()
        self.assertEqual(hook.type, HOOK_NEEDLE_TYPE[0][0])
        self.assertEqual(hook.hook_size, HOOK_SIZE[0][0])
        self.assertIsNone(hook.needle_size)

    def test_pattern_hooks_needle_form_missing_type(self):
        form = PatternHooksNeedleForm(data={
            'hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'needle_size': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)
        self.assertEqual(form.errors['type'], ['This field is required.'])

    def test_pattern_hooks_needle_form_invalid_hook_size(self):
        form = PatternHooksNeedleForm(data={
            'type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'hook_size': 99,  # Invalid hook size
            'needle_size': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('hook_size', form.errors)
        self.assertEqual(form.errors['hook_size'], [
                         'Select a valid choice. 99 is not one of the '
                         'available choices.'])

    def test_pattern_hooks_needle_form_invalid_needle_size(self):
        form = PatternHooksNeedleForm(data={
            'type': HOOK_NEEDLE_TYPE[1][0],  # Needle
            'hook_size': '',
            'needle_size': 99  # Invalid needle size
        })
        self.assertFalse(form.is_valid())
        self.assertIn('needle_size', form.errors)
        self.assertEqual(form.errors['needle_size'], [
                         'Select a valid choice. 99 is not one of the '
                         'available choices.'])


class PatternHooksNeedleFormSetTest(TestCase):
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

    def test_pattern_hooks_needle_formset_valid_data(self):
        formset = PatternHooksNeedleFormSet(data={
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'pattern_hooks_needles-0-hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'pattern_hooks_needles-0-needle_size': '',
        })
        self.assertTrue(formset.is_valid())
        instances = formset.save(commit=False)
        for instance in instances:
            instance.pattern = self.pattern
            instance.save()
        self.assertEqual(PatternHooksNeedle.objects.count(), 1)
        self.assertEqual(PatternHooksNeedle.objects.first().type,
                         HOOK_NEEDLE_TYPE[0][0])
        self.assertEqual(
            PatternHooksNeedle.objects.first().hook_size, HOOK_SIZE[0][0])
        self.assertIsNone(PatternHooksNeedle.objects.first().needle_size)

    def test_pattern_hooks_needle_formset_missing_type(self):
        formset = PatternHooksNeedleFormSet(data={
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-hook_size': HOOK_SIZE[0][0],  # 2.0 mm
            'pattern_hooks_needles-0-needle_size': '',
        })
        self.assertFalse(formset.is_valid())
        self.assertIn('type', formset.errors[0])
        self.assertEqual(formset.errors[0]['type'], [
                         'This field is required.'])

    def test_pattern_hooks_needle_formset_invalid_hook_size(self):
        formset = PatternHooksNeedleFormSet(data={
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-type': HOOK_NEEDLE_TYPE[0][0],  # Hook
            'pattern_hooks_needles-0-hook_size': 99,  # Invalid hook size
            'pattern_hooks_needles-0-needle_size': '',
        })
        self.assertFalse(formset.is_valid())
        self.assertIn('hook_size', formset.errors[0])
        self.assertEqual(formset.errors[0]['hook_size'], [
                         'Select a valid choice. 99 is not one of the '
                         'available choices.'])

    def test_pattern_hooks_needle_formset_invalid_needle_size(self):
        formset = PatternHooksNeedleFormSet(data={
            'pattern_hooks_needles-TOTAL_FORMS': '1',
            'pattern_hooks_needles-INITIAL_FORMS': '0',
            'pattern_hooks_needles-MIN_NUM_FORMS': '0',
            'pattern_hooks_needles-MAX_NUM_FORMS': '1000',
            'pattern_hooks_needles-0-type': HOOK_NEEDLE_TYPE[1][0],  # Needle
            'pattern_hooks_needles-0-hook_size': '',
            'pattern_hooks_needles-0-needle_size': 99,  # Invalid needle size
        })
        self.assertFalse(formset.is_valid())
        self.assertIn('needle_size', formset.errors[0])
        self.assertEqual(formset.errors[0]['needle_size'], [
                         'Select a valid choice. 99 is not one of the '
                         'available choices.'])


class CommentFormTest(TestCase):
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

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'content': 'This is a test comment.'
        })
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        comment.author = self.user
        comment.pattern = self.pattern
        comment.save()
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.pattern, self.pattern)

    def test_comment_form_missing_content(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])

    def test_comment_form_empty_content(self):
        form = CommentForm(data={
            'content': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'], ['This field is required.'])
