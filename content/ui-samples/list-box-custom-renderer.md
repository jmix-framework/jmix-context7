<Path>Components > ListBox > ListBox with custom renderer</Path>

It is possible to customize the render of elements. You can use the setRenderer() method or @Supply annotation for it.

list-box-custom-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="list-box-custom-renderer">
        <listBox id="listBox"/>
    </layout>
</view>




ListBoxCustomRendererSample.java

package io.jmix.uisamples.view.flowui.components.listbox.customrenderer;

import com.vaadin.flow.component.avatar.Avatar;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.data.renderer.ComponentRenderer;
import com.vaadin.flow.server.streams.DownloadHandler;
import io.jmix.core.Resources;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.listbox.JmixListBox;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.record.Simpson;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("list-box-custom-renderer")
@ViewDescriptor("list-box-custom-renderer.xml")
public class ListBoxCustomRendererSample extends StandardView {

    protected static final String PATH_PREFIX = "/META-INF/resources/icons/";

    @ViewComponent
    protected JmixListBox<Simpson> listBox;

    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected Resources resources;

    @Subscribe
    protected void onInit(InitEvent event) {
        listBox.setItems(getListBoxItems());
    }

    @Supply(to = "listBox", subject = "renderer")
    protected ComponentRenderer<HorizontalLayout, Simpson> listBoxRenderer() {
        return new ComponentRenderer<>(simpson -> {
            HorizontalLayout row = uiComponents.create(HorizontalLayout.class);
            row.setAlignItems(FlexComponent.Alignment.CENTER);

            Avatar avatar = uiComponents.create(Avatar.class);
            avatar.setImageHandler(getSimpsonImageHandler(simpson));

            Span name = new Span(simpson.name());
            Span shortName = new Span(simpson.shortName());
            shortName.addClassNames("short-name");

            VerticalLayout column = uiComponents.create(VerticalLayout.class);
            column.add(name, shortName);
            column.setPadding(false);
            column.setSpacing(false);

            row.add(avatar, column);
            row.addClassName("row");
            return row;
        });
    }

    protected List<Simpson> getListBoxItems() {
        return List.of(
                new Simpson("Homer Jay Simpson", "Homer", "homer-simpson.png"),
                new Simpson("Marjorie Jacqueline Simpson", "Marge", "marge-simpson.png"),
                new Simpson("Bartholomew Jojo Simpson", "Bart", "bart-simpson.png")
        );
    }

    protected DownloadHandler getSimpsonImageHandler(Simpson simpson) {
        String picture = simpson.picture();
        return DownloadHandler.forClassResource(getClass(), PATH_PREFIX + picture);
    }
}




Simpson.java

package io.jmix.uisamples.record;

public record Simpson(String name, String shortName, String picture) {
}




list-box-custom-renderer.css


.list-box-custom-renderer .short-name {
    color: var(--vaadin-text-color-secondary);
    font-size: var(--aura-font-size-s);
}

.list-box-custom-renderer .row {
    line-height: var(--aura-line-height-m);
}

