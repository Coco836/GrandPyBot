import views
import pytest
import urllib.request
from unittest.mock import Mock

# @pytest.fixture
# def client():
#     db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
#     flaskr.app.config['TESTING'] = True

#     with flaskr.app.test_client() as client:
#         with flaskr.app.app_context():
#             flaskr.init_db()
#         yield client

#     os.close(db_fd)
#     os.unlink(flaskr.app.config['DATABASE'])

# with app.test_client() as c:
#     data = c.post('/', json={
#         'user_input': 'rzlmmkrlmkzlm', 
#         'message': 'Je ne sais pas de quoi tu parles petit ! Pose moi une vraie question.'
#     })
#     json_data = data.get_json()
#     assert verify_data(user_input, message)