<Path>Components > PasswordField > Simple PasswordField</Path>

PasswordField is a standard TextField with the hidden input.

password-field-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <passwordField id="passwordField" label="PasswordField"/>
    </layout>
</view>




PasswordFieldSimpleSample.java

package io.jmix.uisamples.view.flowui.components.passwordfield.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("password-field-simple")
@ViewDescriptor("password-field-simple.xml")
public class PasswordFieldSimpleSample extends StandardView {
}


