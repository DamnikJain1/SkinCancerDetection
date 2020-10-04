package com.example.skincancer.ui;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.skincancer.R;
import com.example.skincancer.ui.slideshow.SlideshowFragment;

import java.util.Objects;

public class ResultView extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result_view);

        Uri imageUri = Uri.parse(getIntent().getStringExtra("imageUri"));
        final ImageView imageviewRes = findViewById(R.id.imageviewRes);
        imageviewRes.setImageURI(imageUri);

        final String MyPREFERENCES = "MyPrefs" ;
        SharedPreferences sharedpreferences = getSharedPreferences(MyPREFERENCES, Context.MODE_PRIVATE);

        final String SKIN_MESSAGE = "com.example.skincancer.SKIN";
        String skin = sharedpreferences.getString(SKIN_MESSAGE, "NA");
        if (skin.equals("False")){
            final TextView benignView = findViewById(R.id.benignView);
            benignView.setText("Probably Non-Skin Image!");
        }else{
            final String BENIGN_MESSAGE = "com.example.skincancer.BENIGN";
            final String MALIGNANT_MESSAGE = "com.example.skincancer.MALIGNANT";
            double benign_prob = Double.parseDouble(Objects.requireNonNull(sharedpreferences.getString(BENIGN_MESSAGE, "NA")));
            double malignant_prob = Double.parseDouble(Objects.requireNonNull(sharedpreferences.getString(MALIGNANT_MESSAGE, "NA")));

            final TextView benignView = findViewById(R.id.benignView);
            benignView.setText("Benign : "+Math.round(benign_prob* 100000.0) / 1000.0+"%");
            final TextView malignantView = findViewById(R.id.malignantView);
            malignantView.setText("Malignant : "+Math.round(malignant_prob* 100000.0) / 1000.0+"%");
        }


        final Button nearbyButton = findViewById(R.id.nearbyButton);
        nearbyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //launch fragment
                Fragment fragment = new SlideshowFragment();
                getSupportFragmentManager().beginTransaction()
                        .replace(R.id.nav_slideshow, fragment, fragment.getClass().getSimpleName()).addToBackStack(null).commit();
            }
        });

        final Button forumButton = findViewById(R.id.forumButton);
        forumButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //launch fragment
                Fragment fragment = new SlideshowFragment();
                getSupportFragmentManager().beginTransaction()
                        .replace(R.id.nav_send, fragment, fragment.getClass().getSimpleName()).addToBackStack(null).commit();
            }
        });




    }
}
