<Path>Add-ons > Charts > Incremental data update > Automatic data update</Path>

The chart component supports incremental data updating if it is bound with a data provider. The component monitors changes occurring in the data container (collection) and sends the difference in data to the client-side. In this sample, the data is automatically updated using the timer facet.

automatic-data-update.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="transportDc" class="io.jmix.uisamples.entity.TransportCount"
                    fetchPlan="_local">
            <loader id="transportDl" readOnly="true">
                <query>
                    <![CDATA[select e from TransportCount e order by e.year]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
        <timer id="timer"
               delay="2000"
               autostart="false"
               repeating="true"/>
    </facets>
    <layout>
        <hbox padding="false">
            <button id="startStopDataGen"/>
        </hbox>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Transport count" right="10%"/>
            <charts:legend/>

            <charts:tooltip trigger="AXIS">
                <charts:formatterFunction>
                    <![CDATA[
                        function (params) {
                              var tar = params[1];

                              return '<b>Year:</b> ' + tar.name + '<br/><hr/>' +
                              '<b>Cars:</b> ' + tar.value.cars + '<br/>' +
                              '<b>Motorcycles:</b> ' + tar.value.motorcycles + '<br/>' +
                              '<b>Bicycles:</b> ' + tar.value.bicycles + '<br/>';
                            }
                    ]]>
                </charts:formatterFunction>
                <charts:axisPointer type="SHADOW"/>
            </charts:tooltip>

            <charts:xAxes>
                <charts:xAxis/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="transportDc" categoryField="year"
                               valueFields="cars, motorcycles, bicycles"/>
            </charts:dataSet>

            <charts:series>
                <charts:bar name="Car sells"/>
                <charts:bar name="Motorcycle sells"/>
                <charts:bar name="Bicycle sells"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




AutomaticDataUpdateSample.java

package io.jmix.uisamples.view.flowui.charts.incrementalupdate.automaticupdate;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.chartsflowui.component.Chart;
import io.jmix.core.Metadata;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.TransportCount;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Random;

@ViewController("automatic-data-update")
@ViewDescriptor("automatic-data-update.xml")
public class AutomaticDataUpdateSample extends StandardView {

    @Autowired
    private Metadata metadata;

    @ViewComponent
    private CollectionContainer<TransportCount> transportDc;
    @ViewComponent
    private Chart chart;
    @ViewComponent
    private Timer timer;
    @ViewComponent
    private JmixButton startStopDataGen;

    private Integer baseYear = 2013;
    private final Random random = new Random();
    private boolean timerStarted;

    @Subscribe
    private void onInit(InitEvent event) {
        prepareTimerButtonToStart();
    }

    @Subscribe(id = "startStopDataGen", subject = "clickListener")
    public void onStartStopDataGenClick(final ClickEvent<JmixButton> event) {
        if (timerStarted) {
            timer.stop();
            prepareTimerButtonToStart();
        } else {
            timer.start();
            prepareTimerButtonToStop();
        }

        timerStarted = !timerStarted;
    }

    @Subscribe("timer")
    private void onTimerTick(Timer.TimerActionEvent event) {
        removeData();
        addData();
    }

    private void prepareTimerButtonToStart() {
        startStopDataGen.setText("Start");
        startStopDataGen.setIcon(VaadinIcon.PLAY.create());
        startStopDataGen.addThemeVariants(ButtonVariant.PRIMARY);
        startStopDataGen.removeThemeVariants(ButtonVariant.ERROR);
    }

    private void prepareTimerButtonToStop() {
        startStopDataGen.setText("Stop");
        startStopDataGen.setIcon(VaadinIcon.PAUSE.create());
        startStopDataGen.addThemeVariants(ButtonVariant.ERROR);
    }

    private void addData() {
        TransportCount transportCount = metadata.create(TransportCount.class);

        transportCount.setYear(baseYear++);
        transportCount.setCars(random.nextInt(100, 1700));
        transportCount.setMotorcycles(random.nextInt(200, 700));
        transportCount.setBicycles(random.nextInt(5, 100));

        transportDc.getMutableItems().add(transportCount);
    }

    private void removeData() {
        transportDc.getMutableItems().remove(0);
    }
}




TransportCount.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@Table(name = "TRANSPORT_COUNT")
@Entity
@JmixEntity
public class TransportCount {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @NotNull
    @Column(name = "YEAR_", nullable = false)
    private Integer year;

    @NotNull
    @Column(name = "CARS", nullable = false)
    private Integer cars;

    @NotNull
    @Column(name = "MOTORCYCLES", nullable = false)
    private Integer motorcycles;

    @NotNull
    @Column(name = "BICYCLES", nullable = false)
    private Integer bicycles;

    public Integer getBicycles() {
        return bicycles;
    }

    public void setBicycles(Integer bicycles) {
        this.bicycles = bicycles;
    }

    public Integer getMotorcycles() {
        return motorcycles;
    }

    public void setMotorcycles(Integer motorcycles) {
        this.motorcycles = motorcycles;
    }

    public Integer getCars() {
        return cars;
    }

    public void setCars(Integer cars) {
        this.cars = cars;
    }

    public Integer getYear() {
        return year;
    }

    public void setYear(Integer year) {
        this.year = year;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


