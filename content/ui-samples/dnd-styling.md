<Path>Cookbook > Drag and Drop > Drag and Drop styling</Path>

This sample shows how to add visual feedback during dragging with CSS.

While a drag is in progress, Vaadin automatically adds the `v-dragged` class to the dragged component and the `v-drag-over-target` class to a drop target the pointer hovers over. Styling these classes gives the user feedback without any extra Java code.


dnd-styling.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="dnd-styling">
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
                <span text="Drop items here" classNames="dnd-zone-hint"/>
            </vbox>
        </hbox>
    </layout>
</view>




DndStylingSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.styling;

import com.vaadin.flow.component.dnd.DragSource;
import com.vaadin.flow.component.dnd.DropTarget;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.view.*;

import java.util.List;

@ViewController("dnd-styling")
@ViewDescriptor("dnd-styling.xml")
public class DndStylingSample extends StandardView {

    @ViewComponent
    private Div card1;
    @ViewComponent
    private Div card2;
    @ViewComponent
    private Div card3;

    @ViewComponent
    private VerticalLayout dropZone;

    @Subscribe
    public void onInit(InitEvent event) {
        List.of(card1, card2, card3).forEach(DragSource::create);

        DropTarget<VerticalLayout> dropTarget = DropTarget.create(dropZone);
        dropTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent()
                        .ifPresent(dropZone::add));
    }
}




dnd-styling.css


.dnd-styling .dnd-panel {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-styling .dnd-zone {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px dashed var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-styling .dnd-card {
    padding: var(--vaadin-padding-s) var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color);
    border-radius: var(--vaadin-radius-l);

    background: var(--vaadin-background-container);
    cursor: grab;
    user-select: none;
}

.dnd-styling .dnd-card:active {
    cursor: grabbing;
}

.dnd-styling .dnd-zone-hint {
    color: var(--vaadin-text-color-secondary);
}

.dnd-styling .v-dragged {
    opacity: 0.5;
}

.dnd-styling .v-drag-over-target {
    outline: 2px solid var(--aura-accent-color);
    outline-offset: 2px;
    background: color-mix(in srgb, var(--aura-accent-color) 10%, transparent);
}


