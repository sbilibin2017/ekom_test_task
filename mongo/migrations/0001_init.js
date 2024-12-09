db.createUser(
    {
        user: "test",
        pwd: "test",
        roles: [
            {
                role: "readWrite",
                db: "ecom_test_task"
            }
        ]
    }
);