def test_task_create_requires_title(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "", 
         "status": "todo"},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_requires_status(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": ""},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_requires_title_status_none(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "", 
         "status": ""},
        format="json",
    )

    assert res.status_code == 400



def test_task_create_due_date(
        auth_client,
        user
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": "doing",
         "due_date": "2000-01-01"},
        format="json",
    )

    assert res.status_code == 400

def test_task_create_due_date_success(
        auth_client,
        user
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {"title": "DRF勉強", 
         "status": "doing",
         "due_date": "2111-01-01"},
        format="json",
    )

    assert res.status_code == 201


def test_task_status_choice_no_exists(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.post(
        "/api/tasks/",
        {
            "title": "DRF",
            "status": "complete"
        },
        format="json",
        )

    assert res.status_code == 400


def test_task_patch_invalid_status(
    auth_client,
    user,
    task_factory,
):
    task = task_factory(user)

    client = auth_client(user, "password123")

    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"status": "complete"},
        format="json",
    )
    
    assert res.status_code == 400
    task.refresh_from_db()
    assert task.status != "complete"




def test_task_detail_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.get(
        "/api/tasks/99999/"
     )

    assert res.status_code == 404

def test_task_patch_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.patch(
        "/api/tasks/99999/",
        {"title": "updated"},
        format="json",
        )

    assert res.status_code == 404

def test_task_delete_not_found(
    auth_client,
    user,
):
    client = auth_client(user, "password123")

    res = client.delete(
        "/api/tasks/99999/"
        )

    assert res.status_code == 404

