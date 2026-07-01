<Path>Fragments > Fragment events</Path>

A fragment can subscribe to some events in its lifecycle, as well as in the lifecycle of its host-view. The following events are available for subscription: Fragment.ReadyEvent View.InitEvent (host) View.BeforeShowEvent (host) View.ReadyEvent (host) Fragment.ReadyEvent - an event that is fired after the fragment and all its declaratively defined inner components are created, fully initialized and dependency injection completed. Event subscriptions are implemented in such a way that the listeners defined in the host-view are executed first, and then in the fragment. Note that when creating the fragment programmatically, the View.InitEvent event listener for host-view was not executed. This happened because at that moment the fragment was created and the View.InitEvent event has already fired.

fragment-events.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <h4 text="The sequence of events when the fragment created declaratively"/>
        <fragment id="declarativeFragment" class="io.jmix.uisamples.view.flowui.fragments.events.EventsFragment"/>
        <hr/>
        <h4 text="The sequence of events when the fragment created programmatically on InitEvnet"/>
    </layout>
</view>




FragmentEventsSample.java

package io.jmix.uisamples.view.flowui.fragments.events;

import io.jmix.flowui.Fragments;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("fragment-events")
@ViewDescriptor("fragment-events.xml")
public class FragmentEventsSample extends StandardView {

    @Autowired
    protected Fragments fragments;

    @ViewComponent
    protected EventsFragment declarativeFragment;

    protected EventsFragment programmaticFragment;

    @Subscribe
    public void onInit(InitEvent event) {
        programmaticFragment = fragments.create(this, EventsFragment.class);
        getContent().add(programmaticFragment);

        programmaticFragment.addExecutedEvent("View init event");
        declarativeFragment.addExecutedEvent("View init event");
    }

    @Subscribe
    public void onBeforeShow(BeforeShowEvent event) {
        programmaticFragment.addExecutedEvent("View before show event");
        declarativeFragment.addExecutedEvent("View before show event");
    }

    @Subscribe
    public void onReady(ReadyEvent event) {
        programmaticFragment.addExecutedEvent("View ready event");
        declarativeFragment.addExecutedEvent("View ready event");
    }
}




events-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <content>
        <hbox padding="false" classNames="horizontal-layout"/>
    </content>
</fragment>




EventsFragment.java

package io.jmix.uisamples.view.flowui.fragments.events;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.dom.ThemeList;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.Target;
import io.jmix.flowui.view.View;

@FragmentDescriptor("events-fragment.xml")
public class EventsFragment extends Fragment<HorizontalLayout> {

    @Subscribe
    public void onReady(ReadyEvent event) {
        addExecutedEvent("Fragment ready event");
    }

    @Subscribe(target = Target.HOST_CONTROLLER)
    public void onHostInit(View.InitEvent event) {
        addExecutedEvent("Host init event");
    }

    @Subscribe(target = Target.HOST_CONTROLLER)
    public void onHostBeforeShow(View.BeforeShowEvent event) {
        addExecutedEvent("Host before show event");
    }

    @Subscribe(target = Target.HOST_CONTROLLER)
    public void onHostReady(View.ReadyEvent event) {
        addExecutedEvent("Host ready event");
    }

    public void addExecutedEvent(String eventName) {
        Span span = new Span(eventName);

        ThemeList themeList = span.getElement().getThemeList();
        themeList.add("badge");

        if (eventName.contains("Fragment")) {
            themeList.add("error");
        } else if (eventName.contains("View")) {
            themeList.add("success");
        }

        getContent().add(span);
    }
}


