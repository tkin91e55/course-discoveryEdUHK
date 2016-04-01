from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from course_discovery.apps.catalogs.models import Catalog
from course_discovery.apps.course_metadata.models import(
    Course, Image, Organization, Prerequisite, Subject, Video
)


class TimestampModelSerializer(serializers.ModelSerializer):
    modified = serializers.DateTimeField()


class NamedModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta(object):
        fields = ('name', )


class SubjectSerializer(NamedModelSerializer):
    class Meta(NamedModelSerializer.Meta):
        model = Subject


class PrerequisiteSerializer(NamedModelSerializer):
    class Meta(NamedModelSerializer.Meta):
        model = Prerequisite


class MediaSerializer(serializers.ModelSerializer):
    src = serializers.CharField()
    description = serializers.CharField()


class ImageSerializer(MediaSerializer):
    height = serializers.IntegerField()
    width = serializers.IntegerField()

    class Meta(object):
        model = Image
        fields = ('src', 'description', 'height', 'width')


class VideoSerializer(MediaSerializer):
    image = ImageSerializer()

    class Meta(object):
        model = Video
        fields = ('src', 'description', 'image', )


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    logo_image = ImageSerializer()
    description = serializers.CharField()
    homepage_url = serializers.CharField()

    class Meta(object):
        model = Organization
        fields = ('name', 'description', 'logo_image', 'homepage_url', )


class CatalogSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Catalog
        fields = ('id', 'name', 'query', 'courses_count',)


class CourseSerializer(TimestampModelSerializer):
    level_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
    subjects = SubjectSerializer(many=True)
    prerequisites = PrerequisiteSerializer(many=True)
    expected_learning_items = serializers.SlugRelatedField(many=True, read_only=True, slug_field='value')
    image = ImageSerializer()
    video = VideoSerializer()
    owners = OrganizationSerializer(many=True)
    sponsors = OrganizationSerializer(many=True)

    class Meta(object):
        model = Course
        fields = (
            'key', 'title', 'short_description', 'full_description', 'level_type', 'subjects',
            'prerequisites', 'expected_learning_items', 'image', 'video', 'owners', 'sponsors',
            'modified',
        )


class ContainedCoursesSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    courses = serializers.DictField(
        child=serializers.BooleanField(),
        help_text=_('Dictionary mapping course IDs to boolean values')
    )
