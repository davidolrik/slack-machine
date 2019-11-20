from dataclasses import dataclass
from typing import Optional, Dict
from dacite import from_dict


@dataclass
class Profile:
    avatar_hash: str
    status_text: str
    status_emoji: str
    status_expiration: int
    real_name: str
    display_name: str
    real_name_normalized: str
    display_name_normalized: str
    email: Optional[str]
    image_original: Optional[str]
    image_24: str
    image_32: str
    image_48: str
    image_72: str
    image_192: str
    image_512: str
    team: str


@dataclass
class User:
    id: str
    team_id: str
    name: str
    deleted: bool
    color: Optional[str]
    real_name: Optional[str]
    tz: Optional[str]
    tz_label: Optional[str]
    tz_offset: Optional[int]
    profile: Profile
    is_admin: Optional[bool]
    is_owner: Optional[bool]
    is_primary_owner: Optional[bool]
    is_restricted: Optional[bool]
    is_ultra_restricted: Optional[bool]
    is_bot: bool
    is_stranger: Optional[bool]
    updated: int
    is_app_user: bool
    has_2fa: Optional[bool]
    locale: Optional[str]

    @staticmethod
    def from_api_response(user_reponse: Dict) -> 'User':
        return from_dict(data_class=User, data=user_reponse)


class UserSearchDict(dict):
    def find(self, search_string: str) -> Optional[User]:
        # Find the user by ID
        user = self.get(search_string)
        if user:
            return user
        else:
            # If the user can't be found by ID, try searching by name
            for id, user in self.items():
                if str(user.name) == search_string:
                    return user