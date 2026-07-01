<Path>Components > TextField > Simple TextField</Path>

TextField can be used both for working with entity attributes and entering/displaying arbitrary textual information. If a text field is linked to an entity attribute (via dataContainer and property), and if the entity attribute has a length parameter defined in the @Column JPA-annotation, then the TextField will limit the maximum length of entered text accordingly. If a text field is not linked to an attribute, or if the attribute does not have length value defined, or this value needs to be overridden, then the maximum length of the entered text can be limited using maxLength attribute.

text-field-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <textField id="textField" label="TextField"/>
        <textField id="textLengthField" label="MaxLength = 10" maxLength="10"/>
    </layout>
</view>




TextFieldSimpleSample.java

package io.jmix.uisamples.view.flowui.components.textfield.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-field-simple")
@ViewDescriptor("text-field-simple.xml")
public class TextFieldSimpleSample extends StandardView {
}


