import uuid

from django.utils import timezone


def auto_create_matricule(user_type):
    valid_user_types = ["staff", "student"]
    st_pre_string = "ST"
    teach_pre_string = "TC-"
    # The post string should eventaully come from the settings.
    # And the length of the unique string should aswell come from the settings.
    post_string = "-HT"
    year = str(timezone.now().date().year)[-2:]
    unique_string = str(uuid.uuid4())[-6:]
    if user_type in valid_user_types:
        if user_type == "staff":
            # Control the prefix of the matricule based on teacher or student.
            matricule = (
                teach_pre_string + "-" + year + "-" + unique_string + post_string
            )
        elif user_type == "student":
            matricule = st_pre_string + "-" + year + "-" + unique_string + post_string
        else:
            raise ValueError(
                "Invalid user type, user type should be 'staff or student'"
            )
    else:
        raise ValueError("Invalid user type")

    return matricule.upper()
