<Path>Components > ProgressBar > ProgressBar with ThemeVariant</Path>

The ProgressBar component has several theme variants: success error contrast You can set these styles to the ProgressBar component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ProgressBarVariant class.

progress-bar-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="progress-bar-theme-variant-layout">
        <checkbox id="indeterminateCheckbox" label="Indeterminate" value="true"/>
        <h4 id="standardSpan" text="Standard"/>
        <progressBar id="standardProgressBar" indeterminate="true"/>
        <h4 id="successSpan" text="Success"/>
        <progressBar id="successProgressBar" indeterminate="true" themeNames="success"/>
        <h4 id="warningSpan" text="Warning"/>
        <progressBar id="warningProgressBar" indeterminate="true" themeNames="warning"/>
        <h4 id="errorSpan" text="Error"/>
        <progressBar id="errorProgressBar" indeterminate="true" themeNames="error"/>
    </layout>
</view>




ProgressBarThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.progressbar.themevariant;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.progressbar.ProgressBar;
import io.jmix.flowui.backgroundtask.BackgroundTask;
import io.jmix.flowui.backgroundtask.BackgroundTaskHandler;
import io.jmix.flowui.backgroundtask.BackgroundWorker;
import io.jmix.flowui.backgroundtask.TaskLifeCycle;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;
import java.util.concurrent.TimeUnit;

@ViewController("progress-bar-theme-variant")
@ViewDescriptor("progress-bar-theme-variant.xml")
public class ProgressBarThemeVariantSample extends StandardView {

    private static final int ITERATIONS = 20;

    @ViewComponent
    private ProgressBar standardProgressBar;
    @ViewComponent
    private ProgressBar successProgressBar;
    @ViewComponent
    private ProgressBar warningProgressBar;
    @ViewComponent
    private ProgressBar errorProgressBar;

    @Autowired
    private BackgroundWorker backgroundWorker;

    private BackgroundTaskHandler<Void> taskHandler;
    private Collection<ProgressBar> progressBars;

    @Subscribe
    public void onInit(InitEvent event) {
        progressBars = List.of(standardProgressBar, successProgressBar, warningProgressBar, errorProgressBar);
    }

    @Subscribe("indeterminateCheckbox")
    public void onIndeterminateCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        Boolean value = event.getValue();

        if (value && taskHandler != null && taskHandler.isAlive()) {
            taskHandler.cancel();
        } else if (!value){
            runNewTask();
        }

        progressBars.forEach(progressBar -> progressBar.setIndeterminate(value));
    }

    private void runNewTask() {
        taskHandler = backgroundWorker.handle(createBackgroundTask());
        taskHandler.execute();
    }

    private BackgroundTask<Integer, Void> createBackgroundTask() {
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
                progressBars.forEach(progressBar -> progressBar.setValue(lastValue / ITERATIONS));
            }
        };
    }
}


