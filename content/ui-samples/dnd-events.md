<Path>Cookbook > Drag and Drop > Drag and Drop events</Path>

This sample subscribes to every drag-and-drop event and shows a notification for each one.

A `DragSource` fires `DragStartEvent` when dragging begins and `DragEndEvent` when it ends — use `isSuccessful()` to tell a completed drop from a cancelled drag. A `DropTarget` fires `DropEvent` when the user drops on it.

`Drag sources` and `Drop zone` are drop targets, so a card can be dragged between them to fire `Dropped` and a successful `Drag ended`. `Cannot drop here` is not a drop target, so dropping a card on it produces no `Dropped` event and a cancelled `Drag ended`.


dnd-events.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="dnd-events">
        <hbox width="100%" height="100%">
            <vbox id="sourcePanel" classNames="dnd-panel" minHeight="20em">
                <span text="Drag sources" classNames="bold"/>
                <div id="card1" classNames="dnd-card">
                    <span text="Item 1"/>
                </div>
                <div id="card2" classNames="dnd-card">
                    <span text="Item 2"/>
                </div>
                <div id="card3" classNames="dnd-card">
                    <span text="Item 3"/>
                </div>
            </vbox>
            <vbox id="dropZone" classNames="dnd-zone" minHeight="20em">
                <span text="Drop zone" classNames="bold"/>
            </vbox>
            <vbox id="cannotDropZone" classNames="dnd-zone" minHeight="20em">
                <span text="Cannot drop here" classNames="bold"/>
            </vbox>
        </hbox>
    </layout>
</view>




DndEventsSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.events;

import com.vaadin.flow.component.dnd.DragEndEvent;
import com.vaadin.flow.component.dnd.DragSource;
import com.vaadin.flow.component.dnd.DragStartEvent;
import com.vaadin.flow.component.dnd.DropEvent;
import com.vaadin.flow.component.dnd.DropTarget;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("dnd-events")
@ViewDescriptor("dnd-events.xml")
public class DndEventsSample extends StandardView {

    @ViewComponent
    private Div card1;
    @ViewComponent
    private Div card2;
    @ViewComponent
    private Div card3;

    @ViewComponent
    private VerticalLayout sourcePanel;
    @ViewComponent
    private VerticalLayout dropZone;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(InitEvent event) {
        List.of(card1, card2, card3).forEach(this::makeDraggable);

        makeDropTarget(sourcePanel);
        makeDropTarget(dropZone);
    }

    private void makeDraggable(Div card) {
        DragSource<Div> dragSource = DragSource.create(card);
        dragSource.addDragStartListener(this::onDragStart);
        dragSource.addDragEndListener(this::onDragEnd);
    }

    private void makeDropTarget(VerticalLayout zone) {
        DropTarget<VerticalLayout> dropTarget = DropTarget.create(zone);
        dropTarget.addDropListener(dropEvent -> onDrop(dropEvent, zone));
    }

    private void onDragStart(DragStartEvent<Div> event) {
        showNotification("Drag started");
    }

    private void onDrop(DropEvent<VerticalLayout> event, VerticalLayout zone) {
        event.getDragSourceComponent().ifPresent(zone::add);
        showNotification("Dropped");
    }

    private void onDragEnd(DragEndEvent<Div> event) {
        showNotification("Drag ended: " + (event.isSuccessful() ? "successful" : "cancelled"));
    }

    private void showNotification(String message) {
        notifications.create(message)
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }
}




dnd-events.css


.dnd-events .dnd-panel {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-events .dnd-zone {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px dashed var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-events .dnd-card {
    padding: var(--vaadin-padding-s) var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color);
    border-radius: var(--vaadin-radius-l);

    background: var(--vaadin-background-container);
    cursor: grab;
    user-select: none;
}

.dnd-events .dnd-card:active {
    cursor: grabbing;
}


