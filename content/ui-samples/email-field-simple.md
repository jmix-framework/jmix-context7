<Path>Components > EmailField > Simple EmailField</Path>

EmailField is a standard TextField with Email pattern.

email-field-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <emailField id="emailField" label="EmailField"/>
    </layout>
</view>




EmailFieldSimpleSample.java

package io.jmix.uisamples.view.flowui.components.emailfield.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("email-field-simple")
@ViewDescriptor("email-field-simple.xml")
public class EmailFieldSimpleSample extends StandardView {
}


