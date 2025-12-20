<Path>Fragments > Fragment renderer</Path>

The virtualList component supports fragments as renderers. To do this you need to add a nested <fragmentRenderer/> element. Using the class attribute, you must specify the fragment class that extends the special io.jmix.flowui.fragmentrenderer.FragmentRenderer abstract class. Fragment renderer is very similar to a regular fragment. The difference is that the fragmentRenderer can contain an optional instance container in which the item to be renderer will be set. To specify which container an item should be placed in, use the @RendererItemContainer annotation. The container may not be defined, in which case you can use the FragmentRenderer#getItem() method to handle the rendering. List of supported components: VirtualList DataGrid.Column CheckboxGroup MultiSelectComboBox MultiSelectComboBoxPicker EntityComboBox RadioButtonGroup Select ListBox MultiSelectListBox GridLayout

fragment-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="employeesDc"
                    class="io.jmix.uisamples.entity.Employee">
            <fetchPlan extends="_base"/>
            <loader id="employeeDl">
                <query>
                    <![CDATA[select e from Employee e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout alignItems="CENTER">
        <virtualList id="virtualList" width="100%" itemsContainer="employeesDc" alignSelf="CENTER">
            <fragmentRenderer
                    class="io.jmix.uisamples.view.flowui.fragments.renderer.EmployeeInfoFragment"/>
        </virtualList>
    </layout>
</view>




FragmentRendererSample.java

package io.jmix.uisamples.view.flowui.fragments.renderer;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("fragment-renderer")
@ViewDescriptor("fragment-renderer.xml")
public class FragmentRendererSample extends StandardView {
}




EmployeeInfoFragment.java

package io.jmix.uisamples.view.flowui.fragments.renderer;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.fragment.FragmentDescriptor;
import io.jmix.flowui.fragmentrenderer.FragmentRenderer;
import io.jmix.flowui.fragmentrenderer.RendererItemContainer;
import io.jmix.uisamples.entity.Employee;

@FragmentDescriptor("employee-info-fragment.xml")
@RendererItemContainer("employeeDc")
public class EmployeeInfoFragment extends FragmentRenderer<VerticalLayout, Employee> {
}




employee-info-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data readOnly="true">
        <instance id="employeeDc" class="io.jmix.uisamples.entity.Employee"/>
    </data>
    <content>
        <vbox padding="false" spacing="false" classNames="mb-m">
            <div classNames="flex flex-row gap-xs">
                <h3 dataContainer="employeeDc" property="firstName"/>
                <h3 dataContainer="employeeDc" property="lastName"/>
            </div>

            <details summaryText="Address" width="100%">
                <formLayout dataContainer="employeeDc">
                    <textField property="address.zip" readOnly="true"/>
                    <textField property="address.country" readOnly="true"/>
                    <textField property="address.city" readOnly="true"/>
                    <textField property="address.addressLine" readOnly="true"/>
                </formLayout>
            </details>
        </vbox>
    </content>
</fragment>




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.springframework.lang.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}


