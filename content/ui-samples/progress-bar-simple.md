<Path>Components > ProgressBar > Simple ProgressBar</Path>

The ProgressBar component is used to display the progress of a long process. In this example, the ProgressBar is updated by a background task. An indeterminate state of the indicator can be displayed using the indeterminate attribute. Indicator shows an indeterminate state if the attribute value is true. Default is false.

progress-bar-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox padding="false">
            <h4 text="ProgressBar with indicator"/>
            <button id="controlButton"
                    icon="PLAY" themeNames="icon tertiary-inline"/>
        </hbox>
        <hbox padding="false" classNames="justify-between" width="100%">
            <span id="labelSpan" text="Ready to start"/>
            <span id="percentSpan" text="0%"/>
        </hbox>
        <progressBar id="progressBar" width="100%"/>
        <h4 text="Indeterminate ProgressBar"/>
        <progressBar indeterminate="true" width="100%"/>
    </layout>
</view>




ProgressBarSimpleSample.java

package io.jmix.uisamples.view.flowui.components.progressbar.simple;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.progressbar.ProgressBar;
import io.jmix.flowui.backgroundtask.BackgroundTask;
import io.jmix.flowui.backgroundtask.BackgroundTaskHandler;
import io.jmix.flowui.backgroundtask.BackgroundWorker;
import io.jmix.flowui.backgroundtask.TaskLifeCycle;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;
import java.util.concurrent.TimeUnit;

@ViewController("progress-bar-simple")
@ViewDescriptor("progress-bar-simple.xml")
public class ProgressBarSimpleSample extends StandardView {

    protected static final int ITERATIONS = 20;

    @ViewComponent
    protected ProgressBar progressBar;
    @ViewComponent
    protected Span labelSpan;
    @ViewComponent
    protected Span percentSpan;
    @ViewComponent
    protected JmixButton controlButton;

    @Autowired
    protected BackgroundWorker backgroundWorker;

    protected BackgroundTaskHandler<Void> taskHandler;

    protected void runNewTask() {
        taskHandler = backgroundWorker.handle(createBackgroundTask());
        taskHandler.execute();
    }

    protected BackgroundTask<Integer, Void> createBackgroundTask() {
        return new BackgroundTask<>(100, TimeUnit.SECONDS) {

            @Override
            public Void run(TaskLifeCycle<Integer> taskLifeCycle) throws Exception {
                for (int i = 1; i <= ITERATIONS; i++) {
                    TimeUnit.SECONDS.sleep(1);
                    taskLifeCycle.publish(i);
                }

                return null;
            }

            @Override
            public void progress(List<Integer> changes) {
                double lastValue = changes.get(changes.size() - 1);
                double value = lastValue / ITERATIONS;

                if (value < 1) {
                    labelSpan.setText("In progress");
                } else {
                    labelSpan.setText("Done");
                    controlButton.setIcon(VaadinIcon.REFRESH.create());
                }

                progressBar.setValue(value);
                percentSpan.setText(Double.valueOf(value * 100).intValue() + "%");
            }
        };
    }

    @Subscribe("controlButton")
    protected void onControlButtonClick(ClickEvent<JmixButton> event) {
        if (taskHandler == null || taskHandler.isDone() || taskHandler.isCancelled()) {
            runNewTask();

            event.getSource().setIcon(VaadinIcon.STOP.create());
        } else if (taskHandler != null && taskHandler.isAlive()) {
            taskHandler.cancel();

            labelSpan.setText("Canceled");
            event.getSource().setIcon(VaadinIcon.REFRESH.create());
        }
    }
}


