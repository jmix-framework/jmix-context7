<Path>Cookbook > Drag and Drop > Drag and Drop for components</Path>

This sample demonstrates the basic drag-and-drop API for arbitrary components.

Use `DragSource.create()` to make a component draggable and `DropTarget.create()` to turn a layout into a drop target. Both zones are drop targets, so the cards can be dragged from one zone to the other in either direction.

When a card is dropped, `DropEvent.getDragSourceComponent()` returns the dragged component, and adding it to the target zone moves it there from its previous parent.


dnd-components.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="dnd-components">
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
        </hbox>
    </layout>
</view>




DndComponentsSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.components;

import com.vaadin.flow.component.dnd.DragSource;
import com.vaadin.flow.component.dnd.DropTarget;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.view.*;

import java.util.List;

@ViewController("dnd-components")
@ViewDescriptor("dnd-components.xml")
public class DndComponentsSample extends StandardView {

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

    @Subscribe
    public void onInit(InitEvent event) {
        List.of(card1, card2, card3).forEach(DragSource::create);

        makeDropTarget(sourcePanel);
        makeDropTarget(dropZone);
    }

    private void makeDropTarget(VerticalLayout zone) {
        DropTarget<VerticalLayout> dropTarget = DropTarget.create(zone);
        dropTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent()
                        .ifPresent(zone::add));
    }
}




dnd-components.css


.dnd-components .dnd-panel {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-components .dnd-zone {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px dashed var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-components .dnd-card {
    padding: var(--vaadin-padding-s) var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color);
    border-radius: var(--vaadin-radius-l);
    background: var(--vaadin-background-container);

    cursor: grab;
    user-select: none;
}

.dnd-components .dnd-card:active {
    cursor: grabbing;
}


