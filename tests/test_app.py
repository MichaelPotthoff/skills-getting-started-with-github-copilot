from src.app import activities


def test_get_activities_returns_seeded_activities(client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class"}
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert expected_activities.issubset(response_data.keys())
    assert expected_fields.issubset(response_data["Chess Club"].keys())


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_signup_adds_student_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    expected_message = f"Signed up {email} for {activity_name}"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    expected_detail = "Student is already signed up for this activity"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": expected_detail}


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "new.student@mergington.edu"
    expected_detail = "Activity not found"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": expected_detail}


def test_unregister_removes_student_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    expected_message = f"Unregistered {email} from {activity_name}"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    expected_detail = "Student is not signed up for this activity"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": expected_detail}


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "new.student@mergington.edu"
    expected_detail = "Activity not found"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": expected_detail}