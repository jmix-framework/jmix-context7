<Path>Cookbook > Other recipes > Custom login form</Path>

The login view can be styled using CSS. This sample shows a way to place a picture on the background of the login view. Note: the image must be located in the application's theme folder. This way it will be accessible to the client-side of the application.

custom-login.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout padding="false" spacing="false">
        <hr/>
        <div classNames="custom-login">
            <loginForm id="login"
                       rememberMeVisible="false"
                       forgotPasswordButtonVisible="false"
                       localesVisible="false">
                <form title="Custom Login Sample"
                      username="Username"
                      password="Password"
                      rememberMe="Remember me"
                      submit="Log in"
                      forgotPassword="Forgot password"/>
            </loginForm>
        </div>
        <hr/>
    </layout>
</view>





CustomLoginSample.java

package io.jmix.uisamples.view.flowui.cookbook.customlogin;

import com.vaadin.flow.component.Html;
import com.vaadin.flow.component.login.AbstractLogin;
import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.loginform.JmixLoginForm;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("custom-login")
@ViewDescriptor("custom-login.xml")
public class CustomLoginSample extends StandardView {

    @ViewComponent
    protected JmixLoginForm login;

    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(final InitEvent event) {
        login.setUsername("user");
        login.setPassword("user");
    }

    @Subscribe("login")
    protected void onLogin(AbstractLogin.LoginEvent event) {
        Html content = new Html(String.format(getHtmlTemplate(), event.getUsername(), event.getPassword()));

        notifications.create(content)
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .show();

        event.getSource().setEnabled(true);
    }

    protected String getHtmlTemplate() {
        return """
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <b>Let's pretend that you are logged in as:</b>
                    <span><b>Username: </b> %s</span>
                    <span><b>Password: </b> %s</span>
                </div>
                """;
    }
}




custom-login.css


.custom-login {
    width: 100%;
    background-image: url("background.png");
    background-position: center;
    background-size: cover;
    display: flex;
    height: 25em;
}

.custom-login jmix-login-form {
    align-items: center;
    display: flex;
    max-width: 25em;
    background-color: var(--vaadin-background-color);
}

.custom-login vaadin-login-form-wrapper {
    background-image: none;
}

