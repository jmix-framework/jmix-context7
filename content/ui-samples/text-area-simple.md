<Path>Components > TextArea > Simple TextArea</Path>

Text Area is an input field component for multi-line text input. To limit user input use the maxLength attribute.

text-area-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <textArea id="textArea" value="Great job. This is excellent!" label="Comment"
                  valueChangeMode="EAGER" maxLength="140" helperText="29/140"/>
        <textArea id="textArea2" value="Everything you do works great!" label="Additional comment"/>
    </layout>
</view>




TextAreaSimpleSample.java

package io.jmix.uisamples.view.flowui.components.textarea.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.textarea.JmixTextArea;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-area-simple")
@ViewDescriptor("text-area-simple.xml")
public class TextAreaSimpleSample extends StandardView {

    @Subscribe("textArea")
    protected void onTextAreaValueChange(ComponentValueChangeEvent<JmixTextArea, String> event) {
        event.getSource().setHelperText(event.getValue().length() + "/" + 140);
    }
}


