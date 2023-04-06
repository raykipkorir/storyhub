
# follow functionality
def follow_functionality(action, profile, current_user_profile) -> None:
    if action == "follow":
        current_user_profile.follows.add(profile)
    elif action == "unfollow":
        current_user_profile.follows.remove(profile)
    current_user_profile.save()
