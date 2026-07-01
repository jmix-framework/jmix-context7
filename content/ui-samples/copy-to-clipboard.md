<Path>Cookbook > Other recipes > Copying text to the clipboard</Path>

This sample shows the implementation of copying text to the clipboard. This implementation uses an asynchronous JavaScript function call, because copying can only occur on the client-side.

copy-to-clipboard.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <textField id="textField" value="UI Samples">
            <suffix>
                <button id="copyButton" icon="CLIPBOARD_TEXT" classNames="link-button"/>
            </suffix>
        </textField>
    </layout>
</view>




CopyToClipboardSample.java

package io.jmix.uisamples.view.flowui.cookbook.copytoclipboard;

import com.google.common.base.Strings;
import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.UiComponentUtils;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("copy-to-clipboard")
@ViewDescriptor("copy-to-clipboard.xml")
public class CopyToClipboardSample extends StandardView {

    @ViewComponent
    private TypedTextField<String> textField;

    @Autowired
    private Notifications notifications;

    @Subscribe("copyButton")
    public void onCopyButtonClick(ClickEvent<JmixButton> event) {
        String valueToCopy = Strings.nullToEmpty(textField.getTypedValue());

        UiComponentUtils.copyToClipboard(valueToCopy)
                .then(successResult -> notifications.create("Text copied!")
                                .withPosition(Notification.Position.BOTTOM_END)
                                .withThemeVariant(NotificationVariant.SUCCESS)
                                .show(),
                        errorResult -> notifications.create("Copy failed!")
                                .withPosition(Notification.Position.BOTTOM_END)
                                .withThemeVariant(NotificationVariant.ERROR)
                                .show());
    }
}


