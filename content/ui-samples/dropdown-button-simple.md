<Path>Components > DropdownButton > Simple DropdownButton</Path>

DropdownButton is a button with drop-down list of items. The DropdownButton can contain text or icon. The component has several items variants: textItem - contains text. ClickListener can be added from a controller. componentItem - contains a custom component. ClickListener can also be added from a controller. actionItem - can be associated with an action using the ref attribute. separator - just for separating items.

dropdown-button-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <dropdownButton id="dropdownButton1" text="Save">
            <items>
                <textItem id="docSaveItem" text="Save as DOC"/>
                <textItem id="pdfSaveItem" text="Save as PDF"/>
            </items>
        </dropdownButton>
        <dropdownButton id="dropdownButton2" text="Save" icon="ARCHIVE" themeNames="icon">
            <items>
                <componentItem id="docSaveItem">
                    <hbox padding="false">
                        <icon icon="FILE"/>
                        <span text="Save as DOC"/>
                    </hbox>
                </componentItem>
                <componentItem id="pdfSaveItem">
                    <hbox padding="false">
                        <icon icon="FILE"/>
                        <span text="Save as PDF"/>
                    </hbox>
                </componentItem>
            </items>
        </dropdownButton>
        <dropdownButton id="dropdownButton3" icon="ARCHIVE" themeNames="icon"/>
    </layout>
</view>




DropdownButtonSimpleSample.java

package io.jmix.uisamples.view.flowui.components.dropdownbutton.simple;

import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.action.BaseAction;
import io.jmix.flowui.kit.component.dropdownbutton.DropdownButton;
import io.jmix.flowui.kit.component.dropdownbutton.DropdownButtonItem;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("dropdown-button-simple")
@ViewDescriptor("dropdown-button-simple.xml")
public class DropdownButtonSimpleSample extends StandardView {

    @ViewComponent
    protected DropdownButton dropdownButton3;

    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        dropdownButton3.addItem(
                "docSaveItem",
                new BaseAction("docSave")
                        .withText("Save as DOC")
                        .withHandler(e -> saveAsDoc())
        );
        dropdownButton3.addSeparator();
        dropdownButton3.addItem(
                "docPdfItem",
                new BaseAction("pdfSave")
                        .withText("Save as PDF")
                        .withHandler(e -> saveAsPdf())
        );
    }

    @Subscribe("dropdownButton1.docSaveItem")
    protected void onDocSave1ActionPerformed(DropdownButtonItem.ClickEvent event) {
        saveAsDoc();
    }

    @Subscribe("dropdownButton1.pdfSaveItem")
    protected void onPdfSave1ActionPerformed(DropdownButtonItem.ClickEvent event) {
        saveAsPdf();
    }

    @Subscribe("dropdownButton2.docSaveItem")
    protected void onDocSave2ActionPerformed(DropdownButtonItem.ClickEvent event) {
        saveAsDoc();
    }

    @Subscribe("dropdownButton2.pdfSaveItem")
    protected void onPdfSave2ActionPerformed(DropdownButtonItem.ClickEvent event) {
        saveAsPdf();
    }

    protected void saveAsDoc() {
        notifications.create("Saved as DOC")
                .withThemeVariant(NotificationVariant.LUMO_SUCCESS)
                .show();
    }

    protected void saveAsPdf() {
        notifications.create("Saved as PDF")
                .withThemeVariant(NotificationVariant.LUMO_SUCCESS)
                .show();
    }
}


