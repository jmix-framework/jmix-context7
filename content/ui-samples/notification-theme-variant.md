<Path>Dialogs and notifications > Notifications > Notification with ThemeVariant</Path>

The Notifications component has several theme variants and types. Theme Variants: primary success error contrast Types: default success warning error system You can also configure the duration of the notification, or the ability to close. All these settings are available by the fluent Notifications API.

notification-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <vbox width="AUTO" padding="false">
            <details summaryText="Theme Variant" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="standardNotificationButton" text="Standard"/>
                    <button id="primaryNotificationButton" text="Primary" themeNames="primary"/>
                    <button id="successNotificationButton" text="Success" themeNames="success"/>
                    <button id="errorNotificationButton" text="Error" themeNames="error"/>
                    <button id="contrastNotificationButton" text="Contrast" themeNames="contrast"/>
                </hbox>
            </details>

            <details summaryText="Type" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="defaultTypeNotificationButton" text="Default" icon="COMMENT"/>
                    <button id="successTypeNotificationButton" text="Success" icon="CHECK"/>
                    <button id="warningTypeNotificationButton" text="Warning" icon="WARNING"/>
                    <button id="errorTypeNotificationButton" text="Error" icon="EXCLAMATION_CIRCLE"/>
                    <button id="systemTypeNotificationButton" text="System" icon="SERVER"/>
                </hbox>
            </details>

            <details summaryText="Duration and cloesable" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="durationNotificationButton" text="With duration" icon="CLOCK"/>
                    <button id="closeableNotificationButton" text="Closeable" icon="CLOSE"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test notification" opened="true" width="45%">
            <vbox padding="false">
                <button id="testButton" icon="COMMENTS"
                        text="Show notification" themeNames="primary"/>
                <formLayout>
                    <responsiveSteps>
                        <responsiveStep minWidth="0" columns="1"/>
                        <responsiveStep minWidth="25em" columns="2"/>
                    </responsiveSteps>

                    <textField id="titleField" label="Title"/>
                    <textField id="messageField" label="Message"/>
                    <checkbox id="closeableField" label="Closeable"/>
                    <integerField id="durationField" label="Duration"
                                  placeholder="Duration in milliseconds"
                                  helperText="Duration greater than 10 seconds will be ignored">
                        <validators>
                            <max value="10000"/>
                            <min value="0"/>
                        </validators>
                    </integerField>
                    <comboBox id="positionField" label="Position" clearButtonVisible="true"/>
                    <comboBox id="themeVariantField" label="ThemeVariant" clearButtonVisible="true"/>
                    <comboBox id="typeField" label="Type" clearButtonVisible="true"/>
                </formLayout>
                <span text="Be attentive. Some of the settings overlap each other."/>
            </vbox>
        </details>
    </layout>
</view>




NotificationThemeVariantSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.notifications.themevariant;

import com.google.common.base.Strings;
import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.component.textfield.JmixIntegerField;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.LinkedHashMap;
import java.util.Map;

@ViewController("notification-theme-variant")
@ViewDescriptor("notification-theme-variant.xml")
public class NotificationThemeVariantSample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> titleField;
    @ViewComponent
    protected TypedTextField<String> messageField;
    @ViewComponent
    protected JmixCheckbox closeableField;
    @ViewComponent
    protected JmixIntegerField durationField;
    @ViewComponent
    protected JmixComboBox<Notification.Position> positionField;
    @ViewComponent
    protected JmixComboBox<NotificationVariant> themeVariantField;
    @ViewComponent
    protected JmixComboBox<Notifications.Type> typeField;

    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(positionField, getPositionItemsMap());
        ComponentUtils.setItemsMap(themeVariantField, getThemeVariantItemsMap());
        ComponentUtils.setItemsMap(typeField, getTypeItemsMap());

        titleField.setTypedValue("Title");
        messageField.setTypedValue("Message");
    }

    @Subscribe("standardNotificationButton")
    protected void onStandardNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("ThemeVariant: Standard");
    }

    @Subscribe("primaryNotificationButton")
    protected void onPrimaryNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("ThemeVariant: Primary")
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .show();
    }

    @Subscribe("successNotificationButton")
    protected void onSuccessNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("ThemeVariant: Success")
                .withThemeVariant(NotificationVariant.LUMO_SUCCESS)
                .show();
    }

    @Subscribe("errorNotificationButton")
    protected void onErrorNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("ThemeVariant: Error")
                .withThemeVariant(NotificationVariant.LUMO_ERROR)
                .show();
    }

    @Subscribe("contrastNotificationButton")
    protected void onContrastNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("ThemeVariant: Contrast")
                .withThemeVariant(NotificationVariant.LUMO_CONTRAST)
                .show();
    }

    @Subscribe("defaultTypeNotificationButton")
    protected void onDefaultTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Type: Default")
                .withType(Notifications.Type.DEFAULT)
                .show();
    }

    @Subscribe("successTypeNotificationButton")
    protected void onSuccessTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Type: Success")
                .withType(Notifications.Type.SUCCESS)
                .show();
    }

    @Subscribe("warningTypeNotificationButton")
    protected void onWarningTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Type: Warning")
                .withType(Notifications.Type.WARNING)
                .show();
    }

    @Subscribe("errorTypeNotificationButton")
    protected void onErrorTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Type: Error")
                .withType(Notifications.Type.ERROR)
                .show();
    }

    @Subscribe("systemTypeNotificationButton")
    protected void onSystemTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Type: System")
                .withType(Notifications.Type.SYSTEM)
                .show();
    }

    @Subscribe("durationNotificationButton")
    protected void onDurationTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Duration: 5 sec")
                .withDuration(5000)
                .show();
    }

    @Subscribe("closeableNotificationButton")
    protected void onCloseableTypeNotificationButtonClick(ClickEvent<JmixButton> event) {
        notifications.create("Closeable: true")
                .withCloseable(true)
                .show();
    }

    @Subscribe("testButton")
    protected void onTestButtonClick(ClickEvent<JmixButton> event) {
        Notifications.NotificationBuilder notificationBuilder;

        String title = titleField.getTypedValue();
        String message = messageField.getTypedValue();

        if (!Strings.isNullOrEmpty(title) && !Strings.isNullOrEmpty(message)) {
            notificationBuilder = notifications.create(title, message);
        } else if (!Strings.isNullOrEmpty(title)) {
            notificationBuilder = notifications.create(title);
        } else if (!Strings.isNullOrEmpty(message)) {
            notificationBuilder = notifications.create("", message);
        } else {
            notificationBuilder = notifications.create("", "");
        }

        notificationBuilder.withCloseable(closeableField.getValue());

        Integer duration = durationField.getValue();
        if (duration != null && duration < 10000 && duration > 0) {
            notificationBuilder.withDuration(duration);
        }

        Notification.Position position = positionField.getValue();
        if (position != null) {
            notificationBuilder.withPosition(position);
        }

        NotificationVariant themeVariant = themeVariantField.getValue();
        if (themeVariant != null) {
            notificationBuilder.withThemeVariant(themeVariant);
        }

        Notifications.Type type = typeField.getValue();
        if (type != null) {
            notificationBuilder.withType(type);
        }

        notificationBuilder.show();
    }

    protected Map<Notification.Position, String> getPositionItemsMap() {
        LinkedHashMap<Notification.Position, String> map = new LinkedHashMap<>();
        map.put(Notification.Position.TOP_STRETCH, "Top Stretch");
        map.put(Notification.Position.TOP_START, "Top Start");
        map.put(Notification.Position.TOP_CENTER, "Top Center");
        map.put(Notification.Position.TOP_END, "Top End");
        map.put(Notification.Position.MIDDLE, "Middle");
        map.put(Notification.Position.BOTTOM_START, "Bottom Start");
        map.put(Notification.Position.BOTTOM_CENTER, "Bottom Center");
        map.put(Notification.Position.BOTTOM_END, "Bottom End");
        map.put(Notification.Position.BOTTOM_STRETCH, "Bottom Stretch");
        return map;
    }

    protected Map<NotificationVariant, String> getThemeVariantItemsMap() {
        LinkedHashMap<NotificationVariant, String> map = new LinkedHashMap<>();
        map.put(NotificationVariant.LUMO_PRIMARY, "Primary");
        map.put(NotificationVariant.LUMO_SUCCESS, "Success");
        map.put(NotificationVariant.LUMO_ERROR, "Error");
        map.put(NotificationVariant.LUMO_CONTRAST, "Contrast");
        return map;
    }

    protected Map<Notifications.Type, String> getTypeItemsMap() {
        LinkedHashMap<Notifications.Type, String> map = new LinkedHashMap<>();
        map.put(Notifications.Type.DEFAULT, "Default");
        map.put(Notifications.Type.SUCCESS, "Success");
        map.put(Notifications.Type.WARNING, "Warning");
        map.put(Notifications.Type.ERROR, "Error");
        map.put(Notifications.Type.SYSTEM, "System");
        return map;
    }
}


