import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import AboutPage from '../pages/AboutPage';

const AppRoutes = () => (
    <Router>
        <Switch>
            <Route exact path="/" component={HomePage} />
            <Route path="/about" component={AboutPage} />
        </Switch>
    </Router>
);

export default AppRoutes;
