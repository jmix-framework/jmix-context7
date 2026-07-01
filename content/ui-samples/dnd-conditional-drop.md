<Path>Cookbook > Drag and Drop > Drag and Drop by condition</Path>

This sample shows how to allow a drop based on a condition — the dragged item's category.

Each card carries a category set with `DragSource.setDragData()` (`red` or `green`). When a card is dropped, the target reads `DropEvent.getDragData()` and accepts the card only if its category matches the container: red cards can be dropped only into the red container, green cards only into the green one. A drop into the wrong container is rejected and a notification is shown.

This data-driven check runs in the drop listener, so it behaves the same way in every browser.


dnd-conditional-drop.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="dnd-conditional">
        <hbox width="100%" height="100%">
            <vbox id="sourcePanel" classNames="dnd-panel" minHeight="20em">
                <span text="Drag sources" classNames="bold"/>
                <div id="redCard1" classNames="dnd-card dnd-red">
                    <span text="Red 1"/>
                </div>
                <div id="greenCard1" classNames="dnd-card dnd-green">
                    <span text="Green 1"/>
                </div>
                <div id="redCard2" classNames="dnd-card dnd-red">
                    <span text="Red 2"/>
                </div>
                <div id="greenCard2" classNames="dnd-card dnd-green">
                    <span text="Green 2"/>
                </div>
            </vbox>
            <vbox id="redZone" classNames="dnd-zone dnd-red" minHeight="20em">
                <span text="Red items only" classNames="bold"/>
            </vbox>
            <vbox id="greenZone" classNames="dnd-zone dnd-green" minHeight="20em">
                <span text="Green items only" classNames="bold"/>
            </vbox>
        </hbox>
    </layout>
</view>




DndConditionalDropSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.conditional;

import com.vaadin.flow.component.dnd.DragSource;
import com.vaadin.flow.component.dnd.DropTarget;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("dnd-conditional-drop")
@ViewDescriptor("dnd-conditional-drop.xml")
public class DndConditionalDropSample extends StandardView {

    @ViewComponent
    private Div redCard1;
    @ViewComponent
    private Div redCard2;
    @ViewComponent
    private Div greenCard1;
    @ViewComponent
    private Div greenCard2;

    @ViewComponent
    private VerticalLayout redZone;
    @ViewComponent
    private VerticalLayout greenZone;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(InitEvent event) {
        DragSource.create(redCard1).setDragData("red");
        DragSource.create(redCard2).setDragData("red");
        DragSource.create(greenCard1).setDragData("green");
        DragSource.create(greenCard2).setDragData("green");

        configureZone(redZone, "red");
        configureZone(greenZone, "green");
    }

    private void configureZone(VerticalLayout zone, String acceptedCategory) {
        DropTarget<VerticalLayout> dropTarget = DropTarget.create(zone);
        dropTarget.addDropListener(dropEvent -> {
            if (acceptedCategory.equals(dropEvent.getDragData().orElse(null))) {
                dropEvent.getDragSourceComponent().ifPresent(zone::add);
            } else {
                notifications.create("This container accepts only " + acceptedCategory + " items")
                        .withPosition(Notification.Position.BOTTOM_END)
                        .show();
            }
        });
    }
}




dnd-conditional.css


.dnd-conditional .dnd-panel {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-conditional .dnd-zone {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px dashed var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-conditional .dnd-card {
    padding: var(--vaadin-padding-s) var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color);
    border-radius: var(--vaadin-radius-l);
    background: var(--vaadin-background-container);

    cursor: grab;
    user-select: none;
}

.dnd-conditional .dnd-card:active {
    cursor: grabbing;
}

.dnd-conditional .dnd-red {
    border-color: var(--aura-red);
}

.dnd-conditional .dnd-green {
    border-color: var(--aura-green);
}

.dnd-conditional .dnd-card.dnd-red {
    color: var(--aura-red-text);
}

.dnd-conditional .dnd-card.dnd-green {
    color: var(--aura-green-text);
}


