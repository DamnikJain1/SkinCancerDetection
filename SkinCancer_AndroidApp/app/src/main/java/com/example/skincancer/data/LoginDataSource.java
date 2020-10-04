package com.example.skincancer.data;

import android.content.Context;
import android.content.SharedPreferences;

import com.example.skincancer.data.model.LoggedInUser;

import java.io.IOException;
import java.util.UUID;

/**
 * Class that handles authentication w/ login credentials and retrieves user information.
 */
public class LoginDataSource {

    SharedPreferences sharedpreferences;

    static final String Password = "passwordKey";
    static final String Email = "emailKey";
    static final String Uuid = "uuidKey";


    public Result<LoggedInUser> login(SharedPreferences.Editor editor, String username, String password) {
        try {
            String uuid = java.util.UUID.randomUUID().toString();

            editor.putString(Password, password);
            editor.putString(Email, username);
            editor.putString(Uuid, uuid);
            editor.commit();

            LoggedInUser userObj = new LoggedInUser(uuid, username);

            return new Result.Success<>(userObj);
        } catch (Exception e) {
            return new Result.Error(new IOException("Error logging in", e));
        }
    }

    public void logout() {

        return ;
    }
}
