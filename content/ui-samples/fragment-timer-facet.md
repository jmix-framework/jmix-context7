<Path>Fragments > Fragments facets > Timer</Path>

**Timer** is a facet (non-visual component) designed to run UI code at specified time intervals.
The timer action is initiated from the browser as a user request, and its handler can update UI components. The timer
stops working when the fragment it was created for is detached.

Timers are defined using the `timer` element. It has the following attributes:

- `delay` – defines timer interval in milliseconds;
- `autostart` – if set to `true`, the timer starts immediately after the fragment is attached. By
  default, the value is `false`, which means that the timer will start only when its `start()`
  method is invoked;
- `repeating` – turns on repeated execution of the timer. If the attribute is set to `true`,
  the timer runs in cycles at equal intervals defined in the `delay` attribute. Otherwise, the timer runs
  only once – `delay` milliseconds after the timer starts.

To execute code on timer, subscribe to its `TimerActionEvent` in the fragment controller.

See also <a href="/ui-samples/sample/delayed-data-load">the example</a> of how to use timer to delay a costly data
loading operation until the user has made the final choice of conditions.


fragment-timer-facet.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <fragment id="fragment"
                  class="io.jmix.uisamples.view.flowui.fragments.facets.timer.TimerFacetFragment"/>
    </layout>
</view>




FragmentTimerFacetSample.java

package io.jmix.uisamples.view.flowui.fragments.facets.timer;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("fragment-timer-facet")
@ViewDescriptor("fragment-timer-facet.xml")
public class FragmentTimerFacetSample extends StandardView {
}




timer-facet-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <facets>
        <timer id="timer"
               delay="3000"
               autostart="false"
               repeating="true"/>
    </facets>
    <content>
        <vbox classNames="horizontal-layout" alignItems="CENTER" padding="false">
            <button id="timerStartBtn" text="Start" icon="PLAY" themeNames="primary"/>
            <button id="timerStopBtn" text="Stop" icon="PAUSE" themeNames="primary error" enabled="false"/>
            <span id="timerIndicator" text="Timer is ready to start" themeNames="badge contrast pill"/>
        </vbox>
    </content>
</fragment>




TimerFacetFragment.java

package io.jmix.uisamples.view.flowui.fragments.facets.timer;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import org.springframework.beans.factory.annotation.Autowired;

@FragmentDescriptor("timer-facet-fragment.xml")
public class TimerFacetFragment extends Fragment<VerticalLayout> {

    @ViewComponent
    private Timer timer;
    @ViewComponent
    private Span timerIndicator;
    @ViewComponent
    private JmixButton timerStartBtn;
    @ViewComponent
    private JmixButton timerStopBtn;

    @Autowired
    private Notifications notifications;

    private int seconds = 0;
    private int ticks = 0;

    @Subscribe("timerStartBtn")
    public void onStartTimerClick(ClickEvent<JmixButton> event) {
        timer.start();

        timerIndicator.setText("Timer started");
        timerIndicator.getElement().getThemeList().clear();
        timerIndicator.getElement().getThemeList().add("badge pill success");

        notifications.create("Timer started")
                .withPosition(Notification.Position.BOTTOM_END)
                .withThemeVariant(NotificationVariant.SUCCESS)
                .show();

        timerStartBtn.setEnabled(false);
        timerStopBtn.setEnabled(true);
    }

    @Subscribe("timerStopBtn")
    public void onStopTimerClick(ClickEvent<JmixButton> event) {
        timer.stop();
        seconds = 0;

        timerIndicator.setText("Timer stopped");
        timerIndicator.getElement().getThemeList().clear();
        timerIndicator.getElement().getThemeList().add("badge pill error");

        timerStartBtn.setEnabled(true);
        timerStopBtn.setEnabled(false);
    }

    @Subscribe("timer")
    public void onTimerTick(Timer.TimerActionEvent event) {
        ++ticks;
        seconds += event.getSource().getDelay() / 1000;

        notifications.create("Timer tick", seconds + " seconds passed")
                .withDuration(2750)
                .show();
    }

    @Subscribe("timer")
    public void onTimerStop(Timer.TimerStopEvent event) {
        notifications.create("Timer stopped", "Number of ticks: " + ticks)
                .withThemeVariant(NotificationVariant.LUMO_PRIMARY)
                .withDuration(5000)
                .show();
        ticks = 0;
    }
}


