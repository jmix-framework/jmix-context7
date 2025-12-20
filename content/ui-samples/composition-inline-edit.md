<Path>Cookbook > Compositions > Using inline edit</Path>

This sample demonstrates how to use inline editing to reduce the nesting of dialog windows.

Here you can see the same data structure consisting of `Airport`, `Terminal` and `MeetingPoint` entities as in the [2-levels composition]({contextPath}/sample/composition-2-levels) example. The airport detail view displays the list of terminals in the editable data grid. The **Show meeting points** button allows users to view and edit meeting points of a selected terminal.

Implementation details:

- [Airport.java]({currentPath}?tab=Airport.java)
    - `Airport.terminals` attribute is annotated with `@Composition`.

- [Terminal.java]({currentPath}?tab=Terminal.java)
    - `Terminal.meetingPoints` attribute is annotated with `@Composition`.

- [airport-detail-view.xml]({currentPath}?tab=airport-detail-view.xml)
  - `terminalsDataGrid` columns have the `editable="true"` attribute. The data grid also has `editorActionsColumn` for opening and closing inline edit fields for a row.
  - `showMeetingPointsAction` action invokes the selected terminal detail view to show its meeting points.

- [AirportDetailView.java]({currentPath}?tab=AirportDetailView.java) displays airport fields and editable data grid of terminals.
  - `onTerminalsDataGridCreateAction()` handler overrides the default behavior of `terminalsDataGrid.createAction`. Instead of opening a terminal detail view, it creates a new `Terminal` instance, adds it to the data container and invokes inline editing in the data grid.
  - `onTerminalsDataGridShowMeetingPointsAction()` handler is invoked when the user clicks **Show meeting points** button or action in the terminals data grid context menu. It opens [TerminalDetailView]({currentPath}?tab=TerminalDetailView.java) and passes the current `DataContext` to it as a parent. This code demonstrates how to open a nested composition view programmatically.

- [TerminalDetailView.java]({currentPath}?tab=TerminalDetailView.java)
  - This view displays meeting points of a particular terminal. Other attributes of the terminal are edited in the terminals data grid of the airport.
  - `onReady()` event handler updates the dialog title with the name of the edited terminal.
  - `onMeetingPointsDataGridCreateAction()` handler overrides the default behavior of `meetingPointsDataGrid.createAction`. It creates a new meeting point instance, adds it to the collection container and opens the data grid inline editor.
  - `onMeetingPointsDcItemPropertyChange()` event handler marks the root edited `Terminal` entity as modified in `DataContext` when a meeting point's property changes. This ensures all data are saved to the parent `DataContext`.   


Airport.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "AIRPORT", indexes = {
        @Index(name = "IDX_AIRPORT_CITY", columnList = "CITY_ID")
})
@Entity
public class Airport {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "IATA", length = 3)
    private String iata;

    @JoinColumn(name = "CITY_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private City city;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "airport")
    private List<Terminal> terminals;

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }

    public String getIata() {
        return iata;
    }

    public void setIata(String iata) {
        this.iata = iata;
    }

    public List<Terminal> getTerminals() {
        return terminals;
    }

    public void setTerminals(List<Terminal> terminals) {
        this.terminals = terminals;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




Terminal.java

package io.jmix.uisamples.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "TERMINAL", indexes = {
        @Index(name = "IDX_TERMINAL_AIRPORT", columnList = "AIRPORT_ID")
})
@Entity
public class Terminal {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "AIRPORT_ID", nullable = false)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Airport airport;

    @Column(name = "TERMINAL_TYPE", length = 1)
    private String terminalType;

    @Column(name = "GATE_COUNT")
    private Integer gateCount;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "terminal")
    private List<MeetingPoint> meetingPoints;

    public TerminalType getTerminalType() {
        return terminalType == null ? null : TerminalType.fromId(terminalType);
    }

    public void setTerminalType(TerminalType terminalType) {
        this.terminalType = terminalType == null ? null : terminalType.getId();
    }

    public Integer getGateCount() {
        return gateCount;
    }

    public void setGateCount(Integer gateCount) {
        this.gateCount = gateCount;
    }

    public List<MeetingPoint> getMeetingPoints() {
        return meetingPoints;
    }

    public void setMeetingPoints(List<MeetingPoint> meetingPoints) {
        this.meetingPoints = meetingPoints;
    }

    public Airport getAirport() {
        return airport;
    }

    public void setAirport(Airport airport) {
        this.airport = airport;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




MeetingPoint.java

package io.jmix.uisamples.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "MEETING_POINT", indexes = {
        @Index(name = "IDX_MEETING_POINT_TERMINAL", columnList = "TERMINAL_ID")
})
@Entity
public class MeetingPoint {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "DESCRIPTION")
    private String description;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "TERMINAL_ID", nullable = false)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Terminal terminal;

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Terminal getTerminal() {
        return terminal;
    }

    public void setTerminal(Terminal terminal) {
        this.terminal = terminal;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




airport-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://airportDetailView.title"
      focusComponent="form">
    <data>
        <instance id="airportDc"
                  class="io.jmix.uisamples.entity.Airport">
            <fetchPlan extends="_base">
                <property name="city" fetchPlan="_base"/>
                <property name="terminals" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="airportDl"/>
            <collection id="terminalsDc" property="terminals"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="airportDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <textField id="iataField" property="iata"/>
            <entityComboBox id="cityField" property="city">
                <actions>
                    <action id="entityClear" type="entity_clear"/>
                </actions>
                <itemsQuery class="io.jmix.uisamples.entity.City" escapeValueForLike="true"
                            searchStringFormat="(?i)%${inputString}%">
                    <fetchPlan extends="_base"/>
                    <query>
                        <![CDATA[select e from City e where e.name like :searchString escape '\' order by e.name]]>
                    </query>
                </itemsQuery>
            </entityComboBox>
        </formLayout>
        <h4 text="msg://io.jmix.uisamples.entity/Airport.terminals"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button action="terminalsDataGrid.createAction"/>
            <button action="terminalsDataGrid.removeAction"/>
            <button action="terminalsDataGrid.showMeetingPointsAction"/>
        </hbox>
        <dataGrid id="terminalsDataGrid" dataContainer="terminalsDc" width="100%" minHeight="10em">
            <actions>
                <action id="createAction" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="terminal-detail-3"/>
                    </properties>
                </action>
                <action id="removeAction" type="list_remove"/>
                <action id="showMeetingPointsAction" type="list_itemTracking" text="msg://showMeetingPointsAction.text"/>
            </actions>
            <columns>
                <column property="name" editable="true"/>
                <column property="terminalType" editable="true"/>
                <column property="gateCount" editable="true"/>
                <editorActionsColumn key="editorActionsColumn">
                    <editButton icon="PENCIL" text="msg:///actions.Edit"/>
                    <closeButton icon="BAN" text="msg://closeButton.text"/>
                </editorActionsColumn>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




AirportDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition5;

import com.vaadin.flow.component.grid.ItemDoubleClickEvent;
import io.jmix.flowui.DialogWindows;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionPropertyContainer;
import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Airport;
import io.jmix.uisamples.entity.Terminal;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController(id = "airport-detail-5")
@ViewDescriptor(path = "airport-detail-view.xml")
@EditedEntityContainer("airportDc")
public class AirportDetailView extends StandardDetailView<Airport> {

    @Autowired
    private DialogWindows dialogWindows;
    @Autowired
    private Notifications notifications;

    @ViewComponent
    private DataGrid<Terminal> terminalsDataGrid;
    @ViewComponent
    private DataContext dataContext;
    @ViewComponent
    private CollectionPropertyContainer<Terminal> terminalsDc;

    @Subscribe("terminalsDataGrid.createAction")
    public void onTerminalsDataGridCreateAction(final ActionPerformedEvent event) {
        if (terminalsDataGrid.getEditor().isOpen()) {
            notifications.show("Close the editor before creating a new entity");
            return;
        }

        // Create a new `Terminal` instance
        Terminal terminal = dataContext.create(Terminal.class);
        terminal.setAirport(getEditedEntity());
        // And add it to the data container
        terminalsDc.getMutableItems().add(terminal);

        // Invoke inline editing in the data grid
        terminalsDataGrid.select(terminal);
        terminalsDataGrid.getEditor().editItem(terminal);
    }

    @Subscribe("terminalsDataGrid.showMeetingPointsAction")
    public void onTerminalsDataGridShowMeetingPointsAction(final ActionPerformedEvent event) {
        Terminal terminal = terminalsDataGrid.getSingleSelectedItem();
        if (terminal == null) {
            return;
        }

        // Open `TerminalDetailView` and pass the current `DataContext` to it as a parent
        // to support composition editing
        DialogWindow<TerminalDetailView> window = dialogWindows.detail(terminalsDataGrid)
                .withViewClass(TerminalDetailView.class)
                .withParentDataContext(dataContext)
                .editEntity(terminal)
                .build();
        window.setWidth("64em");
        window.setResizable(true);
        window.open();
    }

    @Subscribe("terminalsDataGrid")
    public void onTerminalsDataGridItemDoubleClick(final ItemDoubleClickEvent<Terminal> event) {
        terminalsDataGrid.getEditor().editItem(event.getItem());
    }
}




terminal-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://terminalDetailView.title"
      focusComponent="meetingPointsDataGrid">
    <data>
        <instance id="terminalDc"
                  class="io.jmix.uisamples.entity.Terminal">
            <fetchPlan extends="_base">
                <property name="meetingPoints" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="terminalDl"/>
            <collection id="meetingPointsDc" property="meetingPoints"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createButton" action="meetingPointsDataGrid.createAction"/>
            <button id="removeButton" action="meetingPointsDataGrid.removeAction"/>
        </hbox>
        <dataGrid id="meetingPointsDataGrid" dataContainer="meetingPointsDc" width="100%" minHeight="10em">
            <actions>
                <action id="createAction" type="list_create"/>
                <action id="removeAction" type="list_remove"/>
            </actions>
            <columns>
                <column property="name" editable="true"/>
                <column property="description" editable="true"/>
                <editorActionsColumn key="editorActionsColumn">
                    <editButton icon="PENCIL" text="msg:///actions.Edit"/>
                    <closeButton icon="BAN" text="msg://closeButton.text"/>
                </editorActionsColumn>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




TerminalDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition5;

import com.vaadin.flow.component.grid.ItemDoubleClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.model.CollectionPropertyContainer;
import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.MeetingPoint;
import io.jmix.uisamples.entity.Terminal;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController(id = "terminal-detail-5")
@ViewDescriptor(path = "terminal-detail-view.xml")
@EditedEntityContainer("terminalDc")
public class TerminalDetailView extends StandardDetailView<Terminal> {

    @Autowired
    private Notifications notifications;

    @ViewComponent
    private DataGrid<MeetingPoint> meetingPointsDataGrid;
    @ViewComponent
    private CollectionPropertyContainer<MeetingPoint> meetingPointsDc;
    @ViewComponent
    private DataContext dataContext;
    @ViewComponent
    private MessageBundle messageBundle;

    @Override
    public String getPageTitle() {
        return getEditedEntityOrNull() != null
                ? messageBundle.formatMessage("meetingPoints", getEditedEntity().getName())
                : super.getPageTitle();
    }

    @Subscribe("meetingPointsDataGrid.createAction")
    public void onMeetingPointsDataGridCreateAction(final ActionPerformedEvent event) {
        if (meetingPointsDataGrid.getEditor().isOpen()) {
            notifications.show("Close the editor before creating a new entity");
            return;
        }

        // Create a new meeting point instance
        MeetingPoint meetingPoint = dataContext.create(MeetingPoint.class);
        meetingPoint.setTerminal(getEditedEntity());
        // And add it to the collection container
        meetingPointsDc.getMutableItems().add(meetingPoint);

        // Opens the data grid inline editor
        meetingPointsDataGrid.select(meetingPoint);
        meetingPointsDataGrid.getEditor().editItem(meetingPoint);
    }

    @Subscribe("meetingPointsDataGrid")
    public void onMeetingPointsDataGridItemDoubleClick(final ItemDoubleClickEvent<MeetingPoint> event) {
        meetingPointsDataGrid.getEditor().editItem(event.getItem());
    }

    @Subscribe(id = "meetingPointsDc", target = Target.DATA_CONTAINER)
    public void onMeetingPointsDcItemPropertyChange(final InstanceContainer.ItemPropertyChangeEvent<MeetingPoint> event) {
        // Mark the root edited `Terminal` entity as modified in `DataContext`
        // when a meeting point's property changes
        Terminal terminal = getEditedEntity();
        dataContext.setModified(terminal, true);
    }
}


