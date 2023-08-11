from sqlalchemy import Column, Integer, String
from superagi.models.base_model import DBBaseModel
import requests

marketplace_url = "https://app.superagi.com/api"
# marketplace_url = "http://localhost:3000/api"
class Models(DBBaseModel):
    """
    Represents a Model record in the database

    Attributes:
        id (Integer): The unique identifier of the event.
        model_name (String): The name of the model.
        description (String): The description for the model.
        end_point (String): The end_point for the model.
        model_provider_id (Integer): The unique id of the model_provider from the models_config table.
        token_limit (Integer): The maximum number of tokens for a model.
        type (Strng): The place it is added from.
        version (String): The version of the replicate model.
        org_id (Integer): The ID of the organisation.
    """

    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    end_point = Column(String, nullable=False)
    model_provider_id = Column(Integer, nullable=False)
    token_limit = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    version = Column(String, nullable=False)
    org_id = Column(Integer, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Models instance.
        """
        return f"Models(id={self.id}, model_name={self.model_name}, " \
               f"end_point={self.end_point}, model_provider_id={self.model_provider_id}, " \
               f"token_limit={self.token_limit}, " \
               f"type={self.type}, " \
               f"type={self.version}, " \
               f"org_id={self.org_id})"

    @classmethod
    def fetch_marketplace_list(cls, page):
        headers = {'Content-Type': 'application/json'}
        response = requests.get(
            marketplace_url + f"/models_controller/marketplace/list/{str(page)}",
            headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    @classmethod
    def get_model_install_details(cls, session, marketplace_models, organisation):
        installed_models = session.query(Models).filter(Models.org_id == organisation.id).all()
        for knowledge in marketplace_models:
            if knowledge["name"] in [installed_model.name for installed_model in installed_models]:
                knowledge["is_installed"] = True
            else:
                knowledge["is_installed"] = False
        return marketplace_models