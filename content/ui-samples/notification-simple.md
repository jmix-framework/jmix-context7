<Path>Dialogs and notifications > Notifications > Simple notification</Path>

Notifications are simple informational messages displayed in pop-ups. To show a notification, inject the Notifications bean into the view class and use its fluent interface.

notification-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <button id="standardNotificationButton" text="Standard"/>
        <button id="messageNotificationButton" text="With message"/>
        <button id="componentNotificationButton" text="With component"/>
    </layout>
</view>




NotificationSimpleSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.notifications.simple;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.Text;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("notification-simple")
@ViewDescriptor("notification-simple.xml")
public class NotificationSimpleSample extends StandardView {

    @Autowired
    protected Notifications notifications;
    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    private Icons icons;

    @Subscribe("standardNotificationButton")
    protected void onStandardNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("Standard notification");
    }

    @Subscribe("messageNotificationButton")
    protected void onMessageNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("Notification with message", "Message");
    }

    @Subscribe("componentNotificationButton")
    protected void onComponentNotificationButtonClick(ClickEvent<JmixButton> event) {
        HorizontalLayout content = uiComponents.create(HorizontalLayout.class);

        Text text = new Text("Hello world!");
        Component icon = icons.get(JmixFontIcon.SMILEY);

        content.add(text, icon);

        notifications.show(content);
    }
}


