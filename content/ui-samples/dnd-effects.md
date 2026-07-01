<Path>Cookbook > Drag and Drop > Drag and Drop effects</Path>

This sample shows the drop effects: `MOVE`, `COPY`, `LINK`, and `NONE`.

The cards declare `EffectAllowed.ALL` with `DragSource.setEffectAllowed()`, allowing every operation. Each target declares its operation with `DropTarget.setDropEffect()`:

- `Move here` uses `DropEffect.MOVE` — a dropped card is moved out of the source.
- `Copy here` uses `DropEffect.COPY` — a copy is added and the original stays.
- `Link here` uses `DropEffect.LINK` — a link to the card is added and the original stays.
- `No drop` uses `DropEffect.NONE` — the drop is forbidden, so a card cannot be dropped there.

The drop effect controls the cursor shown while dragging over a target and is reported by `DragEndEvent.getDropEffect()`. The operation must be permitted by the source's `EffectAllowed`.


dnd-effects.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="dnd-effects">
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
                <div id="card4" classNames="dnd-card">
                    <span text="Item 4"/>
                </div>
                <div id="card5" classNames="dnd-card">
                    <span text="Item 5"/>
                </div>
                <div id="card6" classNames="dnd-card">
                    <span text="Item 6"/>
                </div>
            </vbox>
            <vbox id="moveZone" classNames="dnd-zone" minHeight="20em">
                <span text="Move here" classNames="bold"/>
            </vbox>
            <vbox id="copyZone" classNames="dnd-zone" minHeight="20em">
                <span text="Copy here" classNames="bold"/>
            </vbox>
            <vbox id="linkZone" classNames="dnd-zone" minHeight="20em">
                <span text="Link here" classNames="bold"/>
            </vbox>
            <vbox id="noneZone" classNames="dnd-zone" minHeight="20em">
                <span text="No drop" classNames="bold"/>
            </vbox>
        </hbox>
    </layout>
</view>




DndEffectsSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.effects;

import com.vaadin.flow.component.Component;
import com.vaadin.flow.component.dnd.DragSource;
import com.vaadin.flow.component.dnd.DropEffect;
import com.vaadin.flow.component.dnd.DropTarget;
import com.vaadin.flow.component.dnd.EffectAllowed;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.view.*;

import java.util.List;

@ViewController("dnd-effects")
@ViewDescriptor("dnd-effects.xml")
public class DndEffectsSample extends StandardView {

    @ViewComponent
    private Div card1;
    @ViewComponent
    private Div card2;
    @ViewComponent
    private Div card3;
    @ViewComponent
    private Div card4;
    @ViewComponent
    private Div card5;
    @ViewComponent
    private Div card6;

    @ViewComponent
    private VerticalLayout moveZone;
    @ViewComponent
    private VerticalLayout copyZone;
    @ViewComponent
    private VerticalLayout linkZone;
    @ViewComponent
    private VerticalLayout noneZone;

    @Subscribe
    public void onInit(InitEvent event) {
        List.of(card1, card2, card3, card4, card5, card6).forEach(card ->
                DragSource.create(card).setEffectAllowed(EffectAllowed.ALL));

        DropTarget<VerticalLayout> moveTarget = DropTarget.create(moveZone);
        moveTarget.setDropEffect(DropEffect.MOVE);
        moveTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent().ifPresent(moveZone::add));

        DropTarget<VerticalLayout> copyTarget = DropTarget.create(copyZone);
        copyTarget.setDropEffect(DropEffect.COPY);
        copyTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent().ifPresent(component -> copyZone.add(copy(component))));

        DropTarget<VerticalLayout> linkTarget = DropTarget.create(linkZone);
        linkTarget.setDropEffect(DropEffect.LINK);
        linkTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent().ifPresent(component -> linkZone.add(link(component))));

        DropTarget<VerticalLayout> noneTarget = DropTarget.create(noneZone);
        noneTarget.setDropEffect(DropEffect.NONE);
        noneTarget.addDropListener(dropEvent ->
                dropEvent.getDragSourceComponent().ifPresent(noneZone::add));
    }

    private Component copy(Component component) {
        Div card = new Div(new Span(component.getElement().getTextRecursively()));
        card.setClassName("dnd-card");
        DragSource.create(card).setEffectAllowed(EffectAllowed.ALL);
        return card;
    }

    private Component link(Component component) {
        Div card = new Div(new Span(component.getElement().getTextRecursively() + " (link)"));
        card.setClassName("dnd-card");
        return card;
    }
}




dnd-effects.css


.dnd-effects .dnd-panel {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-effects .dnd-zone {
    gap: var(--vaadin-gap-s);
    padding: var(--vaadin-padding-m);

    border: 1px dashed var(--vaadin-border-color-secondary);
    border-radius: var(--vaadin-radius-l);

    align-items: stretch;
}

.dnd-effects .dnd-card {
    padding: var(--vaadin-padding-s) var(--vaadin-padding-m);

    border: 1px solid var(--vaadin-border-color);
    border-radius: var(--vaadin-radius-l);

    background: var(--vaadin-background-container);
    cursor: grab;
    user-select: none;
}

.dnd-effects .dnd-card:active {
    cursor: grabbing;
}


