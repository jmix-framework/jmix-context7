<Path>Components > Icon > Simple Icon</Path>

Given sample shows different ways how to create an icon or set them to the component.

icon-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox id="content" padding="false" alignItems="CENTER" wrap="true">
            <button icon="CHECK" themeNames="icon"/>
            <icon icon="vaadin:smiley-o"/>
            <textField id="field" placeholder="Field"/>
        </hbox>
    </layout>
</view>




IconSimpleSample.java

package io.jmix.uisamples.view.flowui.components.icon.simple;

import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;

@ViewController("icon-simple")
@ViewDescriptor("icon-simple.xml")
public class IconSimpleSample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> field;
    @ViewComponent
    protected HorizontalLayout content;

    @Subscribe
    protected void onInit(InitEvent event) {
        field.setSuffixComponent(VaadinIcon.QUESTION_CIRCLE.create());

        Icon icon = ComponentUtils.parseIcon("lumo:user");
        content.add(icon);
    }
}


