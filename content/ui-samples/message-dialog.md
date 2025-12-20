<Path>Dialogs and notifications > Dialogs > Message dialog</Path>

To use a message dialog, simply write: dialogs.createMessageDialog(). The most basic use case for a message dialog is showing some message to the user. Text formatting is available with HTML — the dialog can display HTML content using the withContent() method. Various dialog settings are also available.

message-dialog.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <button id="textButton" text="Plain text" icon="COMMENT"/>
        <button id="htmlButton" text="HTML content" icon="FILE_CODE"/>
        <button id="customSettingsButton" text="Custom settings" icon="COGS"/>
    </layout>
</view>




MessageDialogSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.dialogs.message;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Html;
import io.jmix.flowui.Dialogs;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("message-dialog")
@ViewDescriptor("message-dialog.xml")
public class MessageDialogSample extends StandardView {

    @Autowired
    protected Dialogs dialogs;

    @Subscribe("textButton")
    protected void onTextButtonClick(ClickEvent<JmixButton> event) {
        dialogs.createMessageDialog()
                .withHeader("Confirmation")
                .withText("You clicked the button")
                .open();
    }

    @Subscribe("htmlButton")
    protected void onHtmlButtonClick(ClickEvent<JmixButton> event) {
        Html htmlContent = new Html("<p>Here starts a paragraph. A new line starts after this.<br />" +
                "<b>This text is bold.</b> <i>This text is italic.</i></p>");

        dialogs.createMessageDialog()
                .withHeader("HTML Message")
                .withContent(htmlContent)
                .open();
    }

    @Subscribe("customSettingsButton")
    protected void onCustomSettingsButtonClick(ClickEvent<JmixButton> event) {
        Html htmlContent = new Html("<div><p>Settings applied:</p>" +
                "<ul>" +
                "<li>CloseOnEsc</li>" +
                "<li>CloseOutsizeClick</li>" +
                "<li>Resizable</li>" +
                "</ul></div>");

        dialogs.createMessageDialog()
                .withHeader("Custom Settings")
                .withContent(htmlContent)
                .withCloseOnEsc(true)
                .withCloseOnOutsideClick(true)
                .withResizable(true)
                .open();
    }
}


