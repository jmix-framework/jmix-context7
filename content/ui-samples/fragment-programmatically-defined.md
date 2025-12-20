<Path>Fragments > Programmatically defined Fragment</Path>

Fragments, as UI components, can also be created programmatically. The Fragments bean is used for this. To create a fragment, a host-component is required. This could be another fragment or a view.

fragment-programmatically-defined.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout/>
</view>




FragmentProgrammaticallyDefinedSample.java

package io.jmix.uisamples.view.flowui.fragments.programmatic;

import io.jmix.flowui.Fragments;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.view.flowui.fragments.simple.ButtonSimpleFragment;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("fragment-programmatically-defined")
@ViewDescriptor("fragment-programmatically-defined.xml")
public class FragmentProgrammaticallyDefinedSample extends StandardView {

    @Autowired
    protected Fragments fragments;

    @Subscribe
    public void onInit(InitEvent event) {
        ButtonSimpleFragment fragment = fragments.create(this, ButtonSimpleFragment.class);
        getContent().add(fragment);
    }
}




button-simple-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <content>
        <details opened="true" summaryText="Fragment">
            <hbox>
                <button id="helloButton"
                        text="Say hello!"
                        title="Click me!"/>
                <button id="saveButton1"
                        text="Save"
                        icon="ARCHIVE"/>
                <button id="saveButton2"
                        title="Save"
                        icon="ARCHIVE"/>
            </hbox>
        </details>
    </content>
</fragment>




ButtonSimpleFragment.java

package io.jmix.uisamples.view.flowui.fragments.simple;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.details.JmixDetails;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.fragment.FragmentUtils;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.Subscribe;
import org.springframework.beans.factory.annotation.Autowired;

@FragmentDescriptor("button-simple-fragment.xml")
public class ButtonSimpleFragment extends Fragment<JmixDetails> {

    @Autowired
    protected Notifications notifications;

    @Subscribe("helloButton")
    public void onHelloButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("Hello, world!");
    }

    @Subscribe("saveButton1")
    public void onSaveButton1Click(ClickEvent<JmixButton> event) {
        FragmentUtils.getComponentId(event.getSource())
                .ifPresent(this::save);
    }

    @Subscribe("saveButton2")
    public void onSaveButton2Click(ClickEvent<JmixButton> event) {
        FragmentUtils.getComponentId(event.getSource())
                .ifPresent(this::save);
    }

    protected void save(String id) {
        notifications.show("Save called from " + id);
    }
}


