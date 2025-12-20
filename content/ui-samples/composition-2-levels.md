<Path>Cookbook > Compositions > Simple 2-levels composition</Path>

This sample demonstrates a two-level composition of `Airport`, `Terminal` and `MeetingPoint` entities: the airport contains a collection of terminals which in turn contain collections of meeting points. 

Terminals and meeting points are saved to the database only together with the owning airport, when you click **OK** button in the airport detail view. If you change a terminal or a meeting point and click **OK** in its detail view, but then click **Cancel** in the airport detail view, the changes will not be saved.  

Implementation details: 

- [Airport.java]({currentPath}?tab=Airport.java)
  - `Airport.terminals` attribute is annotated with `@Composition`.

- [Terminal.java]({currentPath}?tab=Terminal.java)
  - `Terminal.meetingPoints` attribute is annotated with `@Composition`.

- [airport-detail-view.xml]({currentPath}?tab=airport-detail-view.xml)
  - The fetch plan for loading `Airport` contains the `Airport.terminals` attribute.
  - A nested collection data container is defined for the `Airport.terminals` attribute. 
  - The data grid displaying terminals is connected to this data container.
  - The `create` and `edit` actions of the terminals data grid open the terminal detail view as a dialog (see `<property name="openMode" value="DIALOG"/>`). 

- [terminal-detail-view.xml]({currentPath}?tab=terminal-detail-view.xml)
  - The fetch plan for loading `Terminal` contains the `Terminal.meetingPoints` attribute.
  - A nested collection data container is defined for the `Terminal.meetingPoints` attribute.
  - The data grid displaying meeting points is connected to this data container.
  - The `create` and `edit` actions of the meeting points data grid open the meeting point detail view as a dialog (see `<property name="openMode" value="DIALOG"/>`).

The use of multiple nested dialog windows might be problematic for users. The following examples illustrate how to minimize the nesting while editing the same data structure:

- [Master-detail on top]({contextPath}/sample/composition-master-detail-1)
- [Master-detail at bottom]({contextPath}/sample/composition-master-detail-2)
- [Using inline edit]({contextPath}/sample/composition-inline-edit)


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
            <button action="terminalsDataGrid.create"/>
            <button action="terminalsDataGrid.edit"/>
            <button action="terminalsDataGrid.remove"/>
        </hbox>
        <dataGrid id="terminalsDataGrid" dataContainer="terminalsDc" width="100%" minHeight="10em">
            <actions>
                <action id="create" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="terminal-detail-2"/>
                    </properties>
                </action>
                <action id="edit" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="terminal-detail-2"/>
                    </properties>
                </action>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="terminalType"/>
                <column property="gateCount"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




AirportDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition2;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Airport;

@ViewController(id = "airport-detail-2")
@ViewDescriptor(path = "airport-detail-view.xml")
@EditedEntityContainer("airportDc")
public class AirportDetailView extends StandardDetailView<Airport> {
}




terminal-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://terminalDetailView.title"
      focusComponent="form">
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
        <formLayout id="form" dataContainer="terminalDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <select id="terminalTypeField" property="terminalType"/>
            <textField id="gateCountField" property="gateCount"/>
        </formLayout>
        <h4 text="msg://io.jmix.uisamples.entity/Terminal.meetingPoints"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createButton" action="meetingPointsDataGrid.create"/>
            <button id="editButton" action="meetingPointsDataGrid.edit"/>
            <button id="removeButton" action="meetingPointsDataGrid.remove"/>
        </hbox>
        <dataGrid id="meetingPointsDataGrid" dataContainer="meetingPointsDc" width="100%" minHeight="10em">
            <actions>
                <action id="create" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="meeting-point-detail-2"/>
                    </properties>
                </action>
                <action id="edit" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="meeting-point-detail-2"/>
                    </properties>
                </action>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="description"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




TerminalDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition2;

import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.MeetingPoint;
import io.jmix.uisamples.entity.Terminal;

@ViewController(id = "terminal-detail-2")
@ViewDescriptor(path = "terminal-detail-view.xml")
@EditedEntityContainer("terminalDc")
public class TerminalDetailView extends StandardDetailView<Terminal> {

    @ViewComponent
    private DataContext dataContext;

    @Subscribe(id = "meetingPointsDc", target = Target.DATA_CONTAINER)
    public void onMeetingPointsDcItemPropertyChange(final InstanceContainer.ItemPropertyChangeEvent<MeetingPoint> event) {
        // Mark the root edited `Terminal` entity as modified in `DataContext`
        // when a meeting point's property changes
        Terminal terminal = getEditedEntity();
        dataContext.setModified(terminal, true);
    }
}




meeting-point-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://meetingPointDetailView.title"
      focusComponent="form">
    <data>
        <instance id="meetingPointDc"
                  class="io.jmix.uisamples.entity.MeetingPoint">
            <fetchPlan extends="_base"/>
            <loader id="meetingPointDl"/>
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
        <formLayout id="form" dataContainer="meetingPointDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <textField id="descriptionField" property="description"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




MeetingPointDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition2;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.MeetingPoint;

@ViewController(id = "meeting-point-detail-2")
@ViewDescriptor(path = "meeting-point-detail-view.xml")
@EditedEntityContainer("meetingPointDc")
public class MeetingPointDetailView extends StandardDetailView<MeetingPoint> {
}


