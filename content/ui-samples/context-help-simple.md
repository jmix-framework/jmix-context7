<Path>Components > ContextHelp > Simple ContextHelp</Path>

The standard way to display helpers is to use the helperText attribute. This attribute is available to fields.

context-help-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox padding="false" classNames="flex-wrap">
            <textField label="Default helper" helperText="Helper text"/>
            <textField label="Helper above" helperText="Helper text" themeNames="helper-above-field"/>
        </hbox>
        <hbox padding="false" classNames="flex-wrap">
            <textField id="notificationField" label="Helper notification"/>
            <textField id="dialogField" label="Helper dialog"/>
        </hbox>
    </layout>
</view>




ContextHelpSimpleSample.java

package io.jmix.uisamples.view.flowui.components.contexthelp.simple;

import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.Dialogs;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("context-help-simple")
@ViewDescriptor("context-help-simple.xml")
public class ContextHelpSimpleSample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> notificationField;
    @ViewComponent
    protected TypedTextField<String> dialogField;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected Notifications notifications;
    @Autowired
    protected Dialogs dialogs;

    @Subscribe
    protected void onInit(InitEvent event) {
        initNotificationField();
        initDialogField();
    }

    protected void initNotificationField() {
        JmixButton helperButton = createHelperButton();
        helperButton.addClickListener(event ->
                notifications.create("This is a helper notification")
                        .withCloseable(true)
                        .show());

        notificationField.setSuffixComponent(helperButton);
    }

    protected void initDialogField() {
        JmixButton helperButton = createHelperButton();
        helperButton.addClickListener(event ->
                dialogs.createMessageDialog()
                        .withText("This is a helper dialog")
                        .open());

        dialogField.setSuffixComponent(helperButton);
    }

    protected JmixButton createHelperButton() {
        JmixButton helperButton = uiComponents.create(JmixButton.class);
        helperButton.setIcon(VaadinIcon.QUESTION_CIRCLE.create());
        helperButton.addThemeVariants(ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_TERTIARY_INLINE);

        return helperButton;
    }
}


