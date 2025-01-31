from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_LEVEL = (
    (0, 'Easy'),
    (1, 'Medium'),
    (2, 'Hard')
)

CRAFT = (
    (0, 'Crochet'),
    (1, 'Knitting')
)

WEIGHT = (
    (0, 'Lace/2 ply'),
    (1, 'Light Fingering/3 ply'),
    (2, 'Fingering/4 ply (14 wpi)'),
    (3, 'Sport/5 ply (12 wpi)'),
    (4, 'DK/8 ply (11 wpi)'),
    (5, 'Aran/10 ply (8 wpi)'),
    (6, 'Chunky/12 ply (7 wpi)'),
    (7, 'Super Chunky/16 ply (5-6 wpi)')
)

HOOK_NEEDLE_TYPE = (
    (0, 'Hook'),
    (1, 'Needle')
)

HOOK_SIZE = (
    (0, '2.0 mm'),
    (1, '2.25 mm'),
    (2, '2.5 mm'),
    (3, '2.75 mm'),
    (4, '3.0 mm'),
    (5, '3.25 mm'),
    (6, '3.5 mm'),
    (7, '3.75 mm'),
    (8, '4.0 mm'),
    (9, '4.5 mm'),
    (10, '5.0 mm'),
    (11, '5.5 mm'),
    (12, '6.0 mm'),
    (13, '6.5 mm'),
    (14, '7.0 mm'),
    (15, '8.0 mm'),
    (16, '9.0 mm'),
    (17, '10.0 mm'),
    (18, '12.0 mm'),
    (19, '15.0 mm'),
    (20, '20.0 mm')
)

NEEDLE_SIZE = (
    (0, '2.0 mm / US 0'),
    (1, '2.25 mm / US 1'),
    (2, '2.5 mm / US 1.5'),
    (3, '2.75 mm / US 2'),
    (4, '3.0 mm / US 2.5'),
    (5, '3.25 mm / US 3'),
    (6, '3.5 mm / US 4'),
    (7, '3.75 mm / US 5'),
    (8, '4.0 mm / US 6'),
    (9, '4.5 mm / US 7'),
    (10, '5.0 mm / US 8'),
    (11, '5.5 mm / US 9'),
    (12, '6.0 mm / US 10'),
    (13, '6.5 mm / US 10.5'),
    (14, '7.0 mm / US 10.75'),
    (15, '8.0 mm / US 11'),
    (16, '9.0 mm / US 13'),
    (17, '10.0 mm / US 15'),
    (18, '12.0 mm / US 17'),
    (19, '15.0 mm / US 19'),
    (20, '20.0 mm / US 36')
)

SIZE = (
    (0, 'One Size'),
    (1, 'XS'),
    (2, 'S'),
    (3, 'M'),
    (4, 'L'),
    (5, 'XL')
)

CATEGORY = (
    (0, 'Clothing'),
    (1, 'Accessories'),
    (2, 'Toys and Hobbies'),
    (3, 'Pet'),
    (4, 'Home')
)


class Pattern(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patterns"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.IntegerField(choices=DIFFICULTY_LEVEL)
    craft = models.IntegerField(choices=CRAFT)
    yarn_weight = models.IntegerField(choices=WEIGHT)
    size = models.IntegerField(choices=SIZE, blank=True, null=True)
    category = models.IntegerField(choices=CATEGORY, blank=True, null=True)
    # pdf_url = models.URLField(max_length=255, blank=True, null=True)
    # images = models.TextField()
    # videos = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} made by {self.author.username}"


class PatternHooksNeedles(models.Model):
    pattern = models.ForeignKey(
        Pattern, on_delete=models.CASCADE, related_name="pattern_hooks_needles")
    type = models.IntegerField(choices=HOOK_NEEDLE_TYPE)
    hook_size = models.IntegerField(choices=HOOK_SIZE, blank=True, null=True)
    needle_size = models.IntegerField(
        choices=NEEDLE_SIZE, blank=True, null=True)

    def __str__(self):
        type_display = dict(HOOK_NEEDLE_TYPE).get(self.type, "Unknown")
        return f"{type_display} for {self.pattern.title} by {self.pattern.author.username}"


class Library(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="libraries")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} library"


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
