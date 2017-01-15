import sqlalchemy as sa
from imgscaler.meta import get_session
from imgscaler.models import Image
from django.conf import settings
import os
from PIL import Image as PILImg
from PIL import ImageEnhance as PILImageEnhance

class ImageService(object):

	@classmethod
	def all(cls):
		dbsession = get_session()
		query = dbsession.query(Image)
		result = query.order_by(sa.asc(Image.id))
		dbsession.close()
		return result

	@classmethod
	def by_id(cls, _id):
		dbsession = get_session()
		query = dbsession.query(Image)
		result = query.get(_id)
		dbsession.close()
		return result

	@classmethod
	def scale_task(cls):
		dbsession = get_session()
		images = dbsession.query(Image).filter((Image.resized_one == None) | (Image.resized_two == None))
		result = 0;
		for image in images:
			image_name = image.orig_content
			original_file = os.path.join(settings.STATIC_DIR, image_name)
			try:
				image_orig = PILImg.open(original_file)
			except IOError:
				continue

			if image.resized_one == None:
				thumb_name = image_name.split('.')[0] + "_thumb_150.jpg"
				thumb_file = os.path.join(settings.STATIC_DIR, thumb_name)
				image_one = image_orig.resize((150, 150), PILImg.ANTIALIAS)
				image_one.save(thumb_file, 'JPEG')
				image.resized_one = thumb_name

			if image.resized_two == None:
				thumb_name2 = image_name.split('.')[0] + "_thumb_50.jpg"
				thumb_file2 = os.path.join(settings.STATIC_DIR, thumb_name2)
				image_two = image_orig.resize((50, 50), PILImg.ANTIALIAS)
				image_two.save(thumb_file2, 'JPEG')
				image.resized_two = thumb_name2
			dbsession.commit()
			result += 1
		dbsession.close()
		return result