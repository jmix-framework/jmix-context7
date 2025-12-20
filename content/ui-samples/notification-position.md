<Path>Dialogs and notifications > Notifications > Notification position</Path>

The Notifications has several position variants: TOP_STRETCH TOP_START TOP_CENTER TOP_END MIDDLE BOTTOM_START BOTTOM_CENTER BOTTOM_END BOTTOM_STRETCH You can set these variants in the view controller using constants from Notification.Position class.

notification-position.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox padding="false" classNames="flex-wrap">
            <button id="standardNotificationButton" text="Standard"/>
            <button id="clickAllButton" text="Click all" icon="BOMB"/>
        </hbox>
        <formLayout id="buttonsLayout">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="3"/>
            </responsiveSteps>

            <button id="topStretchNotificationButton" text="Top Stretch" colspan="3"/>
            <button id="topStartNotificationButton" text="Top Start"/>
            <button id="topCenterNotificationButton" text="Top Center"/>
            <button id="topEndNotificationButton" text="Top End"/>
            <button id="middleNotificationButton" text="Middle" colspan="3"/>
            <button id="bottomStartNotificationButton" text="Bottom Start"/>
            <button id="bottomCenterNotificationButton" text="Bottom Center"/>
            <button id="bottomEndNotificationButton" text="Bottom End"/>
            <button id="bottomStretchNotificationButton" text="Bottom Stretch" colspan="3"/>
        </formLayout>
    </layout>
</view>




NotificationPositionSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.notifications.position;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("notification-position")
@ViewDescriptor("notification-position.xml")
public class NotificationPositionSample extends StandardView {

    @ViewComponent
    protected FormLayout buttonsLayout;

    @Autowired
    protected Notifications notifications;

    @Subscribe("standardNotificationButton")
    protected void onStandardNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("Position: Standard");
    }

    @Subscribe("clickAllButton")
    protected void onClickAllButtonClick(ClickEvent<JmixButton> event) {
        buttonsLayout.getChildren()
                .forEach(button -> ((JmixButton) button).click());
    }

    @Subscribe("topStretchNotificationButton")
    protected void onTopStretchNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Top Stretch")
                .withPosition(Notification.Position.TOP_STRETCH)
                .show();
    }

    @Subscribe("topStartNotificationButton")
    protected void onTopStartNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Top Start")
                .withPosition(Notification.Position.TOP_START)
                .show();
    }

    @Subscribe("topCenterNotificationButton")
    protected void onTopCenterNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Top Center")
                .withPosition(Notification.Position.TOP_CENTER)
                .show();
    }

    @Subscribe("topEndNotificationButton")
    protected void onTopEndNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Top End")
                .withPosition(Notification.Position.TOP_END)
                .show();
    }

    @Subscribe("middleNotificationButton")
    protected void onMiddleNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Middle")
                .withPosition(Notification.Position.MIDDLE)
                .show();
    }

    @Subscribe("bottomStartNotificationButton")
    protected void onBottomStartNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Bottom Start")
                .withPosition(Notification.Position.BOTTOM_START)
                .show();
    }

    @Subscribe("bottomCenterNotificationButton")
    protected void onBottomCenterNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Bottom Center")
                .withPosition(Notification.Position.BOTTOM_CENTER)
                .show();
    }

    @Subscribe("bottomEndNotificationButton")
    protected void onBottomEndNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Bottom End")
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("bottomStretchNotificationButton")
    protected void onBottomStretchNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Position: Bottom Stretch")
                .withPosition(Notification.Position.BOTTOM_STRETCH)
                .show();
    }
}


