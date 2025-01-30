from django.db import models


class DifficultyLevel(models.TextChoices):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'


class Craft(models.TextChoices):
    CROCHET = 'Crochet'
    KNITTING = 'Knitting'


class Weight(models.TextChoices):
    LACE = 'Lace/2 ply'
    LIGHT_FINGERING = 'Light Fingering/3 ply'
    FINGERING = 'Fingering/4 ply (14 wpi)'
    SPORT = 'Sport/5 ply (12 wpi)'
    DK = 'DK/8 ply (11 wpi)'
    ARAN = 'Aran/10 ply (8 wpi)'
    CHUNKY = 'Chunky/12 ply (7 wpi)'
    SUPER_CHUNKY = 'Super Chunky/16 ply (5-6 wpi)'


class HookNeedleType(models.TextChoices):
    HOOK = 'Hook'
    NEEDLE = 'Needle'


class HookSize(models.TextChoices):
    SIZE_2_0 = '2.0 mm'
    SIZE_2_25 = '2.25 mm'
    SIZE_2_5 = '2.5 mm'
    SIZE_2_75 = '2.75 mm'
    SIZE_3_0 = '3.0 mm'
    SIZE_3_25 = '3.25 mm'
    SIZE_3_5 = '3.5 mm'
    SIZE_3_75 = '3.75 mm'
    SIZE_4_0 = '4.0 mm'
    SIZE_4_5 = '4.5 mm'
    SIZE_5_0 = '5.0 mm'
    SIZE_5_5 = '5.5 mm'
    SIZE_6_0 = '6.0 mm'
    SIZE_6_5 = '6.5 mm'
    SIZE_7_0 = '7.0 mm'
    SIZE_8_0 = '8.0 mm'
    SIZE_9_0 = '9.0 mm'
    SIZE_10_0 = '10.0 mm'
    SIZE_12_0 = '12.0 mm'
    SIZE_15_0 = '15.0 mm'
    SIZE_20_0 = '20.0 mm'


class NeedleSize(models.TextChoices):
    SIZE_2_0 = '2.0 mm / US 0'
    SIZE_2_25 = '2.25 mm / US 1'
    SIZE_2_5 = '2.5 mm / US 1.5'
    SIZE_2_75 = '2.75 mm / US 2'
    SIZE_3_0 = '3.0 mm / US 2.5'
    SIZE_3_25 = '3.25 mm / US 3'
    SIZE_3_5 = '3.5 mm / US 4'
    SIZE_3_75 = '3.75 mm / US 5'
    SIZE_4_0 = '4.0 mm / US 6'
    SIZE_4_5 = '4.5 mm / US 7'
    SIZE_5_0 = '5.0 mm / US 8'
    SIZE_5_5 = '5.5 mm / US 9'
    SIZE_6_0 = '6.0 mm / US 10'
    SIZE_6_5 = '6.5 mm / US 10.5'
    SIZE_7_0 = '7.0 mm / US 10.75'
    SIZE_8_0 = '8.0 mm / US 11'
    SIZE_9_0 = '9.0 mm / US 13'
    SIZE_10_0 = '10.0 mm / US 15'
    SIZE_12_0 = '12.0 mm / US 17'
    SIZE_15_0 = '15.0 mm / US 19'
    SIZE_20_0 = '20.0 mm / US 36'


class Size(models.TextChoices):
    ONE_SIZE = 'One Size'
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'


class Category(models.TextChoices):
    CLOTHING = 'Clothing'
    ACCESSORIES = 'Accessories'
    TOYS_AND_HOBBIES = 'Toys and Hobbies'
    PET = 'Pet'
    HOME = 'Home'


class PatternHooksNeedles(models.Model):
    type = models.CharField(max_length=10, choices=HookNeedleType.choices)
    hook_size = models.CharField(
        max_length=10, choices=HookSize.choices, blank=True, null=True)
    needle_size = models.CharField(
        max_length=20, choices=NeedleSize.choices, blank=True, null=True)


class Pattern(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=10, choices=DifficultyLevel.choices)
    craft = models.CharField(max_length=10, choices=Craft.choices)
    yarn_weight = models.CharField(max_length=30, choices=Weight.choices)
    hook_size = models.ForeignKey(
        PatternHooksNeedles, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(
        max_length=10, choices=Size.choices, blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=Category.choices, blank=True, null=True)
    pdf_url = models.URLField(max_length=255, blank=True, null=True)
    images = models.TextField()
    videos = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Library(models.Model):
    user_id = models.IntegerField()
    pattern_id = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user_id = models.IntegerField()
    pattern_id = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
