<Path>Fragments > Simple Fragment</Path>

To create a Fragment, you need to create a class that extends the io.jmix.flowui.fragment.Fragment class. Note that the Fragment is typed by a component, which will be the root for your component. Also, this component must be specified as content in the XML markup. In this case, it is the JmixDetails component. To bind XML file to a fragment-component, use the @FragmentDescriptor annotation (see FragmentSimpleSample.java). To define a Fragment component in a view, use the fragment tag. You will need to provide the fully qualified class name of your fragment (see fragment-simple.xml). Just like for views, fragments have a declarative implementation of subscriptions adn installers for components. You can use @Subscribe, @Install and @Supply annotations for this. Please note that components inside the fragment are not assigned actual IDs. Hidden IDs are set for them, and FragmentUtils is used to work with them. This is done to avoid conflict between the components and their IDs located on host views.

fragment-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <fragment class="io.jmix.uisamples.view.flowui.fragments.simple.ButtonSimpleFragment"/>
    </layout>
</view>




FragmentSimpleSample.java

package io.jmix.uisamples.view.flowui.fragments.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("fragment-simple")
@ViewDescriptor("fragment-simple.xml")
public class FragmentSimpleSample extends StandardView {
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


