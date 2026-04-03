<Path>Dialogs and notifications > Dialogs > Side dialog</Path>

This sample demonstrates how to build a `SideDialog` with custom header and content.

`SideDialog` is useful when you need a context panel without leaving the current view, for example:

1. Quick details or preview.
2. Edit or settings panel while keeping the main page visible.
3. Filters or search options panel.
4. Recent activity, notifications.
5. And other cases.


side-dialog.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="simpleSideDialogButton" text="msg://simpleSideDialogButton.text"/>
    </layout>
</view>



SideDialogSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.dialogs.sidedialog;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.card.Card;
import com.vaadin.flow.component.card.CardVariant;
import com.vaadin.flow.component.html.H2;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.virtuallist.VirtualList;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.theme.lumo.LumoIcon;
import com.vaadin.flow.theme.lumo.LumoUtility;
import io.jmix.flowui.Dialogs;
import io.jmix.flowui.component.sidedialog.SideDialog;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("side-dialog")
@ViewDescriptor("side-dialog.xml")
public class SideDialogSample extends StandardView {

    @Autowired
    private Dialogs dialogs;

    @ViewComponent
    private MessageBundle messageBundle;

    @Subscribe(id = "simpleSideDialogButton", subject = "clickListener")
    public void onSimpleSideDialogButtonClick(final ClickEvent<JmixButton> event) {
        dialogs.createSideDialog()
                .withHorizontalSize("22em")
                .withHeaderProvider(this::createHeader)
                .withContentComponents(createContent())
                .open();
    }

    private HorizontalLayout createHeader(SideDialog sideDialog) {
        HorizontalLayout header = new HorizontalLayout();
        header.setWidthFull();
        header.add(new H2(messageBundle.getMessage("sideDialogHeader")));
        header.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);

        Button closeButton = new Button(LumoIcon.CROSS.create(), event -> sideDialog.close());
        closeButton.addThemeVariants(ButtonVariant.LUMO_TERTIARY, ButtonVariant.LUMO_ICON, ButtonVariant.LUMO_CONTRAST);
        header.add(closeButton);

        return header;
    }

    private Component createContent() {
        VirtualList<String> list = new VirtualList<>();
        list.setWidthFull();
        list.setItems("Item 1", "Item 2", "Item 3");
        list.setRenderer(new ComponentRenderer<>((item -> {
            Card root = new Card();
            root.setTitle(item);
            root.setHeaderSuffix(LumoIcon.CROSS.create());
            root.add(messageBundle.getMessage("activityDescription"));
            root.addThemeVariants(CardVariant.LUMO_HORIZONTAL);
            root.addClassName(LumoUtility.Margin.Bottom.MEDIUM);
            return root;
        })));
        return list;
    }
}


