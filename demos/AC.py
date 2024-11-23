from manim import *

class LRCCircuitWithOscillation(Scene):
    def construct(self):
        # Circuit parameters
        L = 1.0  # Inductance in Henrys
        R = 2.0  # Resistance in Ohms
        C = 0.5  # Capacitance in Farads
        omega = 2 * PI / 5  # Angular frequency of AC source
        Vm = 5.0  # Maximum voltage of the source
        beta = R / (2 * L)  # Damping coefficient

        # Derived parameters
        Im = Vm / R  # Approximation of maximum current amplitude

        # Time tracking
        self.time_tracker = ValueTracker(0)

        # --- Circuit Diagram ---
        ac_source = Circle(radius=0.3, color=YELLOW).move_to(LEFT * 4)
        ac_label = Text("V", font_size=24).move_to(ac_source.get_center())

        inductor = Rectangle(height=0.3, width=1, color=BLUE).next_to(ac_source, RIGHT, buff=1)
        inductor_label = Text("L", font_size=24).next_to(inductor, UP, buff=0.2)

        resistor = Rectangle(height=0.3, width=1.5, color=RED).next_to(inductor, RIGHT, buff=1)
        resistor_label = Text("R", font_size=24).next_to(resistor, UP, buff=0.2)

        capacitor = VGroup(
            Line(ORIGIN, UP * 0.5, color=GREEN),
            Line(UP * 0.5, DOWN * 0.5, color=GREEN),
            Line(DOWN * 0.5, ORIGIN, color=GREEN)
        ).next_to(resistor, RIGHT, buff=1)
        capacitor_label = Text("C", font_size=24).next_to(capacitor, UP, buff=0.2)

        wire1 = Line(ac_source.get_center(), inductor.get_left(), color=WHITE)
        wire2 = Line(inductor.get_right(), resistor.get_left(), color=WHITE)
        wire3 = Line(resistor.get_right(), capacitor.get_left(), color=WHITE)
        wire4 = Line(capacitor.get_right(), RIGHT * 4, color=WHITE)
        wire5 = Line(RIGHT * 4, ac_source.get_center(), color=WHITE)

        circuit = VGroup(ac_source, ac_label, inductor, inductor_label, resistor, resistor_label,
                         capacitor, capacitor_label, wire1, wire2, wire3, wire4, wire5).shift(UP * 2)

        # --- Oscillating Current Indicator ---
        current_indicator = Dot(color=YELLOW).move_to(wire2.get_center())

        def update_current_indicator(indicator):
            time = self.time_tracker.get_value()
            amplitude = Im * np.exp(-beta * time)
            displacement = amplitude * np.cos(omega * time)
            new_x = wire2.get_center()[0] + displacement * 0.5  # Scale for motion
            indicator.move_to([new_x, wire2.get_center()[1], 0])

        current_indicator.add_updater(update_current_indicator)

        # --- Dynamic Current Graph ---
        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[-Im, Im, Im / 2],
            x_length=10,
            y_length=3,
            axis_config={"include_numbers": True},
        ).to_corner(DOWN + LEFT)

        graph_label = axes.get_axis_labels(x_label="Time (t)", y_label="Current (i)")

        def lrc_current(t):
            return Im * np.exp(-beta * t) * np.cos(omega * t)

        current_graph = always_redraw(lambda: axes.plot(
            lambda t: lrc_current(t),
            x_range=[0, self.time_tracker.get_value()],
            color=BLUE
        ))

        # LRC equation text
        lrc_eq = MathTex(r"L\frac{d^2q}{dt^2} + R\frac{dq}{dt} + \frac{q}{C} = V_m \cos(\omega t)")
        lrc_eq.to_corner(UP + RIGHT)

        # Add all components to the scene
        self.add(circuit, axes, graph_label, current_graph, lrc_eq, current_indicator)

        # Animate the time tracker and the scene
        self.play(self.time_tracker.animate.set_value(20), run_time=20, rate_func=linear)

        # Stop updating and wait at the end
        current_indicator.clear_updaters()
        self.wait()
            